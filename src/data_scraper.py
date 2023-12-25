import json
import math

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


MAX_PRODUCTS_PER_PAGE = 36


def scrape_data_from_link(url: str, pbar: tqdm) -> dict[str, Product]:
    """
    Scrapes data from a given URL by iterating through paginated pages.

    Args:
        url (str): The base URL to scrape data from.
        pbar (tqdm): The progress bar object to update.

    Returns:
        dict[str, Product]: A dictionary containing the scraped data, where the key is the product name and the value is a dictionary of product information.
    """
    # https://billyhydemusic.com.au/product-category/guitar-bass?p=2&product_list_limit=48

    all_data = {}
    base_url = url  # Save the base URL before the loop
    page_product_info = {}
    print(f"Scraping data from {base_url}")
    print(f"Total pages: {get_total_pages(base_url)}")

    for page_number in range(1, get_total_pages(base_url) + 1):
        paginated_url = (
            f"{base_url}?p={page_number}&product_list_limit={MAX_PRODUCTS_PER_PAGE}"
        )
        response = requests.get(paginated_url)
        soup = BeautifulSoup(response.text, "html.parser")

        for Product in soup.find_all("div", {"class": "product-item-info"}):
            name = (
                Product.find("span", {"class": "product-name"}).find("a").text.strip()
            )
            price = Product.find("span", {"class": "price"}).text.strip()
            sku = Product.find("span", {"class": "product-sku"}).text.strip()
            product_url = Product.find("span", {"class": "product-name"}).find("a")[
                "href"
            ]

            data = {
                "name": name,
                "price": price,
                "sku": sku,
                "url": product_url,
            }

            # Use the name as the key for the dictionary
            page_product_info[name] = data

        # use update instead of append to avoid duplicates after each page
        all_data.update(page_product_info)

        # Update the progress bar
        pbar.update()

    return page_product_info


def get_total_pages(url: str) -> int:
    """
    Gets the total number of pages for a given URL.

    Args:
        url (str): The URL to get the total number of pages for.

    Returns:
        int: The total number of pages for the given URL.
    """
    # Get the response from the URL
    response = requests.get(url)

    # Create a BeautifulSoup object from the response
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the total number of products
    total_products = soup.find_all("span", {"class": "toolbar-number"})
    last_number = int(total_products[-1].text)

    # Calculate the total number of pages
    total_pages = math.ceil(last_number / MAX_PRODUCTS_PER_PAGE)

    # Return the total number of pages
    return total_pages


def main():
    # Load links from file
    with open("src/links.txt", "r") as f:
        links = [line.strip() for line in f]

    # Get the total number of pages for each link to allow tqdm to be used
    pages_count = 0
    for link in links:
        pages_count += get_total_pages(link)

    # Create a tqdm progress bar
    pbar = tqdm(total=pages_count)

    # Scrape data from each link
    all_data = {}
    for link in links:
        data = scrape_data_from_link(link, pbar)
        for name, product in data.items():
            all_data[name] = product

    # Close the progress bar
    pbar.close()

    # Save data to file at the very end
    with open("data/scraped_data.json", "w") as f:
        json.dump(all_data, f, indent=2)


if __name__ == "__main__":
    main()
