import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

def scrape_amazon(product_name):
    try:
        url = "https://www.amazon.in/s"
        params = {"k": product_name}
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.select("div.s-main-slot div.s-result-item"):
            price = item.select_one(".a-price .a-price-whole")
            if price:
                clean_price = int(re.sub(r"[^\d]", "", price.text.strip()))
                print("Amazon price found:", clean_price)
                return clean_price
        print("No price found on Amazon for:", product_name)
        return None
    except Exception as e:
        print("Amazon scrape error:", e)
        return None


def scrape_flipkart(product_name):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
        }
        search_query = product_name.replace(' ', '+')
        url = f"https://www.flipkart.com/search?q={search_query}"
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.select("div._1AtVbE"):
            price = item.select_one("div._30jeq3")
            if price:
                clean_price = int(re.sub(r"[^\d]", "", price.text.strip()))
                print("Flipkart price found:", clean_price)
                return clean_price
        print("No price found on Flipkart for:", product_name)
        return None
    except Exception as e:
        print("Flipkart scrape error:", e)
        return None

def scrape_blinkit(product_name): return None

def scrape_zepto(product_name):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
        }
        search_query = product_name.replace(' ', '+')
        url = f"https://www.zeptonow.com/search?query={search_query}"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all product containers
        product_containers = soup.find_all('div', class_='ProductCard__Container-sc-1u5u5t4-0')  # Update with actual class

        for container in product_containers:
            title_element = container.find('h2')  # Update with actual tag/class
            price_element = container.find('span', class_='Price__CurrentPrice-sc-1u5u5t4-3')  # Update with actual class

            if title_element and price_element:
                title = title_element.get_text(strip=True)
                price_text = price_element.get_text(strip=True)
                price = int(re.sub(r"[^\d]", "", price_text))
                print("Zepto price found:", price, "for product:", title)
                return price
        print("No price found on Zepto for:", product_name)
        return None
    except Exception as e:
        print("Zepto scrape error:", e)
        return None

def get_lowest_online_price(product_name):
    prices = []
    for fn in [scrape_amazon, scrape_flipkart, scrape_blinkit, scrape_zepto]:
        price = fn(product_name)
        if price:
            prices.append(price)
    return min(prices) if prices else None