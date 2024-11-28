import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_jumia(query, num_pages=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    
    base_url = "https://www.jumia.com/s"
    products = []

    for page in range(1, num_pages + 1):
        params = {"k": query, "page": page}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in items:
            try:
                name = item.h2.text.strip()
            except AttributeError:
                name = None
            
            try:
                price_whole = item.find("span", "a-price-whole")
                price_fraction = item.find("span", "a-price-fraction")
                price = f"{price_whole.text}.{price_fraction.text}" if price_whole and price_fraction else None
            except AttributeError:
                price = None
            
            try:
                rating = item.find("span", "a-icon-alt").text
            except AttributeError:
                rating = None
            
            products.append({"Name": name, "Price": price, "Rating": rating})

    return products


def save_to_csv(products, filename="products.csv"):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    search_term = input("Enter the product to search: ")
    num_pages = int(input("Enter the number of pages to scrape: "))
    data = scrape_jumia(search_term, num_pages)
    save_to_csv(data)
