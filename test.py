import os
import re
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openai
from openai import OpenAIError


# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load URL from file
with open("url.txt", "r") as f:
    URL = f.read().strip()

def generate_bug_id():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"BUG-{timestamp}"

def generate_bug_report(bug_id, title, description, steps, expected, actual, severity="High"):
    prompt = f"""
    Write a detailed QA bug report in this format:

    Bug ID: {bug_id}
    Title: {title}
    Description: {description}
    Severity: {severity}
    Steps to Reproduce:
    {steps}
    Expected Behavior:
    {expected}
    Actual Behavior:
    {actual}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a QA engineer writing a bug report."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.5
        )
        return response.choices[0].message["content"].strip()
    except OpenAIError as e:
        print(f"⚠️ OpenAI API error: {e}")
        return f"""
Bug ID: {bug_id}
Title: {title}
Description: {description}
Severity: {severity}
Steps to Reproduce:
{steps}
Expected Behavior:
{expected}
Actual Behavior:
{actual}

(Note: This report was generated without OpenAI due to API quota limits.)
"""

def test_price_update():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)

        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".text-center.col-4"))
        )

        if not items:
            return None, "No moisturizer items found on the page."

        first_item = items[0]
        add_button = first_item.find_element(By.TAG_NAME, "button")
        p_tags = first_item.find_elements(By.TAG_NAME, "p")

        if len(p_tags) < 2:
            return None, "Cannot extract price. Unexpected structure."

        price_text = p_tags[1].text
        match = re.search(r"Rs\.?\s*(\d+)", price_text)
        if not match:
            return None, f"Could not extract price from text: {price_text}"

        price_value = int(match.group(1))

        # Add the item twice
        add_button.click()
        time.sleep(1)
        add_button.click()
        time.sleep(1)

        # Go to cart
        cart_button = driver.find_element(By.ID, "cart")
        cart_button.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "total")))
        total_price_text = driver.find_element(By.ID, "total").text
        total_price = int(''.join(filter(str.isdigit, total_price_text)))

        expected_price = price_value * 2

        if total_price != expected_price:
            return {
                "bug_id": generate_bug_id(),
                "title": "Cart total price incorrect for multiple same items",
                "description": "Adding the same moisturizer multiple times does not reflect correct total price in cart.",
                "steps": (
                    "1. Go to the moisturizer page.\n"
                    "2. Add the first moisturizer item to the cart twice.\n"
                    "3. Click on the cart button.\n"
                    "4. Check the total price."
                ),
                "expected": f"The total price should be {expected_price} (2 × {price_value}).",
                "actual": f"The total price displayed is {total_price}.",
                "severity": "High"
            }, None

        return None, None

    except Exception as e:
        return None, f"Test failed: {e}"
    finally:
        driver.quit()

def main():
    bug_info, error = test_price_update()
    if error:
        print(f"❌ Error during test: {error}")
        return

    if bug_info:
        report = generate_bug_report(
            bug_id=bug_info["bug_id"],
            title=bug_info["title"],
            description=bug_info["description"],
            steps=bug_info["steps"],
            expected=bug_info["expected"],
            actual=bug_info["actual"],
            severity=bug_info["severity"]
        )

        print("\n✅ Bug Found:\n")
        print(report)

        with open("bug_report.txt", "w") as f:
            f.write(report)

        print("\n📄 Bug report saved to bug_report.txt")
    else:
        print("✅ No bug found. Cart price updates correctly.")

if __name__ == "__main__":
    main()
