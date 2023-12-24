import json

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class Product:
    def __init__(self, name: str, price: float, sku: str, url: str):
        self.name = name
        self.price = price
        self.sku = sku
        self.url = url

    def __repr__(self):
        return f"<Product name={self.name} price={self.price} sku={self.sku} url={self.url}>"


def scrape_data(url: str) -> tuple[dict[str, Product], bool]:
    # https://billyhydemusic.com.au/product-category/guitar-bass?p=2&product_list_limit=36
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    page_product_info = {}
    for Product in soup.find_all("div", {"class": "product-item-info"}):
        name = Product.find("span", {"class": "product-name"}).find("a").text.strip()
        price = Product.find("span", {"class": "price"}).text.strip()
        sku = Product.find("span", {"class": "product-sku"}).text.strip()
        url = Product.find("span", {"class": "product-name"}).find("a")["href"]

        data = {
            "name": name,
            "price": price,
            "sku": sku,
            "url": url,
        }

        # Use the name as the key for the dictionary
        page_product_info[name] = data

    # Check if there is a next page
    next_page = False
    if soup.find("a", {"class": "action next"}):
        next_page = True

    return page_product_info, next_page


LINK_MANIPULATION = "?p=120&product_list_limit=36"


def main():
    # Load links from file
    with open("src/links.txt", "r") as f:
        links = [line.strip() for line in f]

    # Scrape data from each link
    all_data = {}
    print("Scraping data...")
    for link in links:
        data, next_page_exist = scrape_data(link)
        for name, product in data.items():
            all_data[name] = product
        if next_page_exist:
            page_number = 2
            while next_page_exist:
                data, next_page_exist = scrape_data(
                    link + f"?p={page_number}&product_list_limit=36"
                )
                for name, product in data.items():
                    all_data[name] = product
                page_number += 1
                print(f"Scraping page {page_number}...")

    # Check for duplicates
    print("Checking for duplicates...")
    seen_names = set()
    duplicates = set()
    for name in tqdm(all_data):
        if name in seen_names:
            duplicates.add(name)
        else:
            seen_names.add(name)

    if duplicates:
        print(f"Duplicate products found: {duplicates}")

    # Save data to file
    with open("data/scraped_data.json", "w") as f:
        json.dump(all_data, f, indent=2)


if __name__ == "__main__":
    main()
