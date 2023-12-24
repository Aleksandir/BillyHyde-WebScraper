import json

import requests
from bs4 import BeautifulSoup


class Product:
    def __init__(self, name: str, price: float, sku: str, url: str):
        self.name = name
        self.price = price
        self.sku = sku
        self.url = url

    def __repr__(self):
        return f"<Product name={self.name} price={self.price} sku={self.sku} url={self.url}>"


def scrape_data(url: str):
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

    return page_product_info


def main():
    # Load links from file
    with open("src/links.txt", "r") as f:
        links = [line.strip() for line in f]

    # Scrape data from each link
    all_data = []
    for link in links:
        data = scrape_data(link)
        for product in data.values():
            all_data.append(product)

    # Save data to file
    with open("data/scraped_data.json", "w") as f:
        json.dump(all_data, f, indent=2)


if __name__ == "__main__":
    main()
