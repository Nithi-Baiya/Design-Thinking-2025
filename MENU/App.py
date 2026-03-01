import streamlit as st

st.set_page_config(page_title="รายละเอียดสูตร", layout="wide")

# =========================
# 🔒 ตรวจว่ามีสูตรไหม
# =========================
if "selected_recipe" not in st.session_state:
    st.warning("ไม่พบสูตรที่เลือก")
    st.stop()

recipe = st.session_state.selected_recipe

# =========================
# 🖼 helper เลือกรูปตามโปรตีน
# =========================
def get_recipe_image(recipe):
    selected = st.session_state.get("selected", set())

    for protein in recipe.get("protein_options", []):
        if protein in selected:
            return recipe["images"].get(
                protein,
                recipe["images"]["default"]
            )

    return recipe["images"]["default"]

# =========================
# 🎨 HEADER
# =========================
st.title(recipe["name"])
st.image(get_recipe_image(recipe), use_column_width=True)

# =========================
# 📋 ข้อมูลทั่วไป
# =========================
st.subheader("ข้อมูลทั่วไป")

col1, col2, col3 = st.columns(3)

with col1:
    st.write(f"ประเภท: {recipe['type']}")

with col2:
    st.write(f"เวลา: {recipe['time']}")

with col3:
    st.write(f"ระดับความยาก: {recipe['difficulty']}")

# =========================
# 🧺 วัตถุดิบ
# =========================
st.subheader("วัตถุดิบ")

# base ingredients
st.markdown("**วัตถุดิบหลัก**")
for ing in recipe.get("base_ingredients", []):
    st.write("•", ing)

# protein options
if recipe.get("protein_options"):
    st.markdown("**โปรตีนที่ใช้ได้**")
    for p in recipe["protein_options"]:
        st.write("•", p)

# =========================
# 👨‍🍳 วิธีทำ
# =========================
if recipe.get("steps"):
    st.subheader("วิธีทำ")

    for i, step in enumerate(recipe["steps"], start=1):
        st.write(f"{i}. {step}")

# =========================
# 🔙 ปุ่มกลับ
# =========================
if st.button("⬅ กลับหน้าหลัก"):
    st.switch_page("app.py")
