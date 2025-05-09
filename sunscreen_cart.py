import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

wait = WebDriverWait(driver,10)

driver.get("https://weathershopper.pythonanywhere.com/")

driver.find_element(by=By.XPATH,value='/html/body/div[1]/div[3]/div[2]/a/button').click()

driver.implicitly_wait(5)

driver.maximize_window()

try:
    product_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".text-center.col-4")))
    print(f" Found {len(product_cards)} added to page. ")
except:
    print("Failed to add product to list")
    driver.quit()
    exit()

try:
    random_product = random.choice(product_cards)
    add_btn = random_product.find_element(By.TAG_NAME,value='button')
    driver.execute_script("arguments[0].scrollIntoView();", add_btn)
    wait.until(EC.element_to_be_clickable(add_btn)).click()
    print('Random product added to cart')
except Exception as e:
    print(f"❌ Failed to go to cart: {e}")
    driver.quit()
    exit()

try:
    cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Cart')]")))
    cart_btn.click()
    print("Navigated to cart")
except:
    print("Failed to navigate to cart")
    driver.quit()
    exit()

try:
     cart_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@class='table table-striped']//tr[td]")))
     if cart_rows:
         print(f" Prouct is in cart. Total items: {len(cart_rows)}")
     else:
         print("Cart is empty")
except:
    print("Could not verify cart items")

try:
    
    pay_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stripe-button-el")))
    driver.execute_script("arguments[0].scrollIntoView(true);", pay_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", pay_button)
    print("Pay button clicked")
except Exception as e:
    print(f"Failed to click Pay button: {e}")
    driver.quit()
    exit()




driver.quit()
