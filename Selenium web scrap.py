from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

queries = ["laptop", "phones", "watches"]
product_data = []

for query in queries:
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    driver.get(url)
    
    products = driver.find_elements(By.CSS_SELECTOR, ".s-item")
    
    for idx, product in enumerate(products[:500]):
        try:
            title = product.find_element(By.CSS_SELECTOR, ".s-item__title").text
            link = product.find_element(By.CSS_SELECTOR, ".s-item__link").get_attribute("href")
            image_url = product.find_element(By.CSS_SELECTOR, ".s-item__image img").get_attribute("src")
            try:
                rating = product.find_element(By.CSS_SELECTOR, ".s-item__reviews-count").text
            except:
                rating = "No rating available"
            product_data.append({
                "Query": query,
                "Title": title,
                "Link": link,
                "Image URL": image_url,
                "Rating": rating
            })
        except Exception as e:
            print(f"Error processing product {idx + 1}: {e}")
            continue  
             
             

driver.quit()

df = pd.DataFrame(product_data)
excel_file = "Ws.xlsx"
df.to_excel(excel_file, index=False)

print(f"Data saved to {excel_file}")
filtered_df = df[df["Rating"] != "No rating available"]
filtered_excel_file = "Filtered_Ws.xlsx"
filtered_df.to_excel(filtered_excel_file, index=False)

print(f"Filtered data saved to {filtered_excel_file}")

