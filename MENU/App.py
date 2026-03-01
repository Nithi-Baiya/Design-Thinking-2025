import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import os
import time

st.set_page_config(page_title="เมนูวันนี้ จากวัตถุดิบที่มี", layout="wide")

# =========================
# 🌐 SCRAPER
# =========================
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_recipe_links(list_url):
    try:
        response = requests.get(list_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        links = set()
        for a in soup.select("a[href*='cooking.kapook.com/view']"):
            href = a["href"]
            if href.startswith("http"):
                links.add(href)
            else:
                links.add("https://cooking.kapook.com" + href)

        return list(links)

    except:
        return []


def scrape_kapook(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1")
        recipe_name = title.get_text(strip=True) if title else None

        units = [
            "กรัม", "กก.", "ช้อน", "ช้อนโต๊ะ", "ช้อนชา",
            "ถ้วย", "ฟอง", "ชต.", "ชช.", "มล.", "ลิตร"
        ]

        ingredients = []
        for li in soup.find_all("li"):
            text = li.get_text(strip=True)
            if any(unit in text for unit in units):
                if 2 < len(text) < 200:
                    ingredients.append(text)

        ingredients = list(dict.fromkeys(ingredients))

        # steps
        steps = []
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if text.startswith(tuple(str(i) for i in range(1, 10))):
                steps.append(text)

        if not recipe_name or not ingredients:
            return None

        return {
            "name": recipe_name,
            "base_ingredients": ingredients,
            "protein_options": [],
            "images": {"default": None},
            "type": "ไม่ระบุ",
            "difficulty": "ไม่ระบุ",
            "time": "15–30",
            "steps": steps
        }

    except:
        return None


# =========================
# 📦 โหลดข้อมูลครั้งแรก
# =========================
@st.cache_data
def load_recipes():
    list_page = "https://cooking.kapook.com/"
    links = get_recipe_links(list_page)

    recipes = []
    for i, url in enumerate(links[:15]):  # จำกัด 15 สูตรก่อน
        data = scrape_kapook(url)
        if data:
            data["id"] = i + 1
            recipes.append(data)
        time.sleep(0.5)

    return recipes


RECIPES = load_recipes()

# =========================
# 🧠 SESSION STATE
# =========================
if "selected" not in st.session_state:
    st.session_state.selected = set()

if "name_query" not in st.session_state:
    st.session_state.name_query = ""

# =========================
# 🎯 MATCH LOGIC
# =========================
def matches(recipe):
    selected = st.session_state.selected

    if st.session_state.name_query:
        q = st.session_state.name_query.lower()
        searchable = [recipe["name"]] + recipe.get("base_ingredients", [])
        if not any(q in s.lower() for s in searchable):
            return False

    if not selected:
        return True

    match_count = sum(
        any(sel.lower() in ing.lower() for ing in recipe["base_ingredients"])
        for sel in selected
    )

    return match_count > 0


def match_score(recipe):
    selected = st.session_state.selected
    if not selected:
        return 0

    match_count = sum(
        1 for sel in selected
        if any(sel.lower() in ing.lower() for ing in recipe["base_ingredients"])
    )

    return match_count / len(selected)


# =========================
# 🎨 UI
# =========================
st.title("🍽️ เมนูวันนี้ จากวัตถุดิบที่มี (Live Scrape)")

search_val = st.text_input("พิมพ์ชื่อเมนูหรือวัตถุดิบ")
st.session_state.name_query = search_val.lower() if search_val else ""

all_ingredients = sorted(
    {ing for r in RECIPES for ing in r["base_ingredients"]}
)

selected_ings = st.multiselect(
    "เลือกวัตถุดิบ",
    all_ingredients
)

st.session_state.selected = set(selected_ings)

filtered = [r for r in RECIPES if matches(r)]
results = sorted(filtered, key=lambda r: match_score(r), reverse=True)

st.subheader(f"ผลลัพธ์ ({len(results)} รายการ)")

if not results:
    st.info("ไม่พบสูตรที่ตรงกับเงื่อนไข")

cols = st.columns(3)
for idx, recipe in enumerate(results):
    with cols[idx % 3]:
        with st.container(border=True):

            st.subheader(recipe["name"])

            with st.expander("🥕 วัตถุดิบ"):
                for ing in recipe["base_ingredients"]:
                    st.write("-", ing)

            with st.expander("📖 วิธีทำ"):
                for i, step in enumerate(recipe.get("steps", []), start=1):
                    st.write(f"{i}. {step}")

            score = match_score(recipe)
            if st.session_state.selected:
                st.progress(score)
                st.caption(f"ตรงวัตถุดิบ {score*100:.0f}%")
