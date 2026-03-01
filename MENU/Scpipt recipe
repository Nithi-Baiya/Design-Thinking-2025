import requests
from bs4 import BeautifulSoup
import time

def search_and_get_recipe(ingredient):
    # 1. ค้นหาเมนูจากวัตถุดิบ (URL Search ของ Wongnai)
    search_url = f"https://www.wongnai.com/cooking?q={ingredient}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(f"🔍 กำลังค้นหาเมนูที่มี: {ingredient}...")
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # หาลิงก์เมนูแรกที่เจอ
    recipe_link = soup.find('a', href=True, class_=lambda x: x and 'styles__Card' in x)
    
    if not recipe_link:
        # Fallback กรณีโครงสร้าง Class เปลี่ยน
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            if "/recipes/" in link['href']:
                recipe_link = link
                break

    if recipe_link:
        full_url = "https://www.wongnai.com" + recipe_link['href']
        print(f"✅ พบเมนูแนะนำ! กำลังดึงข้อมูลจาก: {full_url}")
        time.sleep(1) # พักเบรกเล็กน้อยกันโดนบล็อก
        display_details(full_url)
    else:
        print("❌ ขออภัย ไม่พบเมนูที่ตรงกับวัตถุดิบของคุณ")

def display_details(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    title = soup.find('h1').text.strip() if soup.find('h1') else "ไม่ระบุชื่อ"
    print(f"\n--- 🌟 เมนู: {title} 🌟 ---")

    # ดึงวัตถุดิบ (ใช้ Selector กว้างๆ เพื่อความชัวร์)
    print("\n[ วัตถุดิบทั้งหมด ]")
    for item in soup.select('div[class*="Ingredient"], ul li'):
        text = item.get_text(strip=True)
        if text: print(f"• {text}")

    # ดึงวิธีทำ
    print("\n[ ขั้นตอนการทำ ]")
    for i, step in enumerate(soup.select('div[class*="Step"]'), 1):
        print(f"{i}. {step.get_text(strip=True)}")

# ทดสอบใช้งาน
my_ingredient = input("ใส่วัตถุดิบที่คุณมี (เช่น หมูสามชั้น, ไข่ไก่): ")
search_and_get_recipe(my_ingredient)
