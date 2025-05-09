import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to get the total price from the cart
def get_total_price(wait):
    try:
        total_price_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h3[contains(@class, 'text-right') and contains(text(), 'Total')]")
        ))
        return total_price_element.text
    except Exception as e:
        pytest.fail(f" Failed to find total price: {e}")
        return None

# Pytest fixture to setup WebDriver
@pytest.fixture
def setup_browser():
    driver = webdriver.Chrome()  # You can specify the path of the ChromeDriver if needed
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://weathershopper.pythonanywhere.com/moisturizer")
        assert "Moisturizer" in driver.title or "Weather" in driver.title, "Website did not load correctly."
        print("Website opened successfully.")
    except Exception as e:
        driver.quit()
        pytest.fail(f" Failed to open the website: {e}")

    yield driver, wait  # Yield the driver and wait object to the test

    driver.quit()  # Quit the driver after the test is done

# Test case for adding the same product twice and checking the total price
def test_cart_price_updates_on_duplicate_product(setup_browser):
    driver, wait = setup_browser

    # Step 1: Add the same product twice
    try:
        product_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".text-center.col-4")))
        assert len(product_cards) > 0, "No products found on the page."
        
        # Click on the "Add" button twice for the first product
        add_button = product_cards[0].find_element(By.TAG_NAME, "button")
        driver.execute_script("arguments[0].scrollIntoView();", add_button)
        wait.until(EC.element_to_be_clickable(add_button))
        add_button.click()  # First click
        time.sleep(1)  # Optional sleep to ensure action is registered
        add_button.click()  # Second click
        print("Product added twice.")
    except Exception as e:
        pytest.fail(f" Failed to add product to cart: {e}")

    # Step 2: Navigate to Cart
    try:
        cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Cart')]")))
        cart_button.click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='table table-striped']")))
        print("Navigated to cart successfully.")
    except Exception as e:
        pytest.fail(f" Failed to load cart page: {e}")

    # Step 3: Validate number of items in cart
    try:
        cart_rows = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@class='table table-striped']//tr[td]")  # Any row with product info
        ))
        assert len(cart_rows) == 2, f" Expected 2 items, found {len(cart_rows)}."
        print(f" Cart has {len(cart_rows)} items.")
    except Exception as e:
        pytest.fail(f" Error validating cart items: {e}")

    # Step 4: Check the total price in the cart
    try:
        total_price_text = get_total_price(wait)
        assert total_price_text, " Total price is not displayed."
        print(f" Total price displayed: {total_price_text}")
    except Exception as e:
        pytest.fail(f" Error in total price: {e}")

    # Step 5: Verify the Checkout button is present
    try:
        checkout_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Checkout')]")))
        assert checkout_button.is_displayed(), " Checkout button is not visible!"
        print("Checkout button found.")
    except Exception as e:
        pytest.fail(f" Error checking Checkout button: {e}")
