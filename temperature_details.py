from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu") 


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get("https://weathershopper.pythonanywhere.com/")

title = driver.find_element(By.TAG_NAME, "h2")
print(title.text)

driver.implicitly_wait(5)

weather = driver.find_element(By.XPATH, value = '//*[@id="weather"]')
print(weather.text)

driver.implicitly_wait(5)


# Close the browser
driver.quit()
