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
    """
    Scrapes data from a given URL and returns a tuple containing a dictionary of product information and a boolean indicating if there is a next page.

    Args:
        url (str): The URL to scrape data from.

    Returns:
        tuple[dict[str, Product], bool]: A tuple containing a dictionary of product information and a boolean indicating if there is a next page.
    """
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


def scrape_and_add_data(link):
    """
    Scrapes data from a given link and adds it to a dictionary.

    Args:
        link (str): The URL of the webpage to scrape.

    Returns:
        dict: A dictionary containing the scraped data, where the keys are the names and the values are the products.
    """
    # Call the scrape_data function to get the initial data and check if there is a next page
    data, next_page_exist = scrape_data(link)

    # Create an empty dictionary to store the scraped data
    page_data = {}

    # Iterate over the data dictionary and add each name and product to the page_data dictionary
    for name, product in data.items():
        page_data[name] = product

    # Check if there is a next page
    if next_page_exist:
        page_number = 2

        # Continue scraping until there are no more pages
        while next_page_exist:
            # Call the scrape_data function with the URL of the next page
            data, next_page_exist = scrape_data(
                link + f"?p={page_number}&product_list_limit=36"
            )

            # Iterate over the data dictionary and add each name and product to the page_data dictionary
            for name, product in data.items():
                page_data[name] = product

            # Increment the page number for the next iteration
            page_number += 1

            # Print the progress
            print(f"Scraping page {page_number} of {link}...")

    # Return the final page_data dictionary
    return page_data


def main():
    # todo: for each link in links.txt, find the number of pages so that tqdm can be used
    # todo: for each page where the number is checked, save the soup to a file so that another request doesn't have to be made

    # Load links from file
    with open("src/links.txt", "r") as f:
        links = [line.strip() for line in f]

    # Scrape data from each link
    all_data = {}
    for link in tqdm(links):
        data = scrape_and_add_data(link)
        for name, product in data.items():
            all_data[name] = product

    duplicate_check()

    # Save data to file
    with open("data/scraped_data.json", "w") as f:
        json.dump(all_data, f, indent=2)


def duplicate_check(file_path: str = "data/scraped_data.json"):
    """
    Check for duplicate products in the scraped data.

    Args:
        file_path (str): The path to the JSON file containing the scraped data.

    Returns:
        None
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    seen_names = set()
    duplicates = set()
    for name in tqdm(data):
        if name in seen_names:
            duplicates.add(name)
        else:
            seen_names.add(name)

    if duplicates:
        print(f"Duplicate products found: {duplicates}")


if __name__ == "__main__":
    main()
