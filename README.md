# AI Enhanced Bug Report in ECommerce

# WeatherShopper Automation

This project uses **Selenium with Python** to automate the shopping process on [WeatherShopper](https://weathershopper.pythonanywhere.com/), an e-commerce demo site for testing automation tools.

## Features

- Opens the moisturizer or sunscreen page
- Adds a product to the cart
- Navigates to the cart
- Clicks the **"Pay with Card"** button (Stripe integration)
- (Optional) Fills out the Stripe payment form (disabled in this version)

## 🧑‍💻 Scenarios Covered

1. **Website Launch and Temperature Check**  
   - Upon clicking the website link, the temperature of the location is **automatically visible** as part of the page loading process.

2. **Sunscreen Product Button**  
   - When the user clicks the **Sunscreen product button**, a **random item is added to the cart**. This is done automatically through the script to simulate a real user selecting a product.

3. **Moisturizer Button and Cart Bug**  
   - When the user clicks the **Moisturizer button** and selects the **same item twice**, it **throws a bug**. The bug is that the **price does not increase** even when the same product is added multiple times. This bug has been identified in the shopping cart functionality.

## Bug Found through Automation

When adding a product to the cart twice (or more), the **price of the product does not increase** as expected. This is a bug on the website where the price remains fixed even though multiple items are added to the cart. It may affect users who intend to purchase more than one unit of the same product.

##  Requirements

- Python 3.7+
- Google Chrome
- ChromeDriver (matching your browser version)
- Selenium

## Installation

1. **Clone this repository**:
    ```bash
    git clone https://github.com/your-username/weathershopper-automation.git
    cd weathershopper-automation
    ```

2. **Install dependencies**:
    ```bash
    pip install selenium
    ```

3. **Download ChromeDriver**:
    - Get the version matching your Chrome from: https://sites.google.com/chromium.org/driver/
    - Place it in your PATH or project folder.

## Usage

Run the automation script with:

```bash
python weathershopper_bot.py
