import requests
from bs4 import BeautifulSoup

def get_detailed_ingredients(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    print(f"\n📋 รายการวัตถุดิบและปริมาณ:")
    print("-" * 40)

    # ค้นหา Container ของวัตถุดิบ
    # หมายเหตุ: Class Name อาจเปลี่ยนแปลงได้ตามการอัปเดตของเว็บ
    ingredient_items = soup.find_all('div', class_=lambda x: x and 'IngredientItem' in x)

    if not ingredient_items:
        # วิธีสำรอง: ค้นหาจากโครงสร้าง List ทั่วไป
        ingredient_items = soup.select('ul > li')

    for item in ingredient_items:
        # ดึงชื่อวัตถุดิบ
        name = item.find('span', class_=lambda x: x and 'name' in x.lower())
        # ดึงปริมาณ
        amount = item.find('span', class_=lambda x: x and 'unit' in x.lower())

        if name and amount:
            print(f"🔹 {name.get_text(strip=True)} : {amount.get_text(strip=True)}")
        else:
            # ถ้าแยกไม่ออก ให้ดึงข้อความทั้งหมดในแถวนั้น
            print(f"🔹 {item.get_text(separator=' ', strip=True)}")

# ตัวอย่างการใช้งาน
url = "https://www.wongnai.com/recipes/ugc/0984814c62254f6786a344933a39e71b"
get_detailed_ingredients(url)
