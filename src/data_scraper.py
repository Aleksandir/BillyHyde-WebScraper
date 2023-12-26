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


def create_product_from_div(product_div):
    """
    Create a Product object from a given product_div.

    Args:
        product_div (BeautifulSoup): The BeautifulSoup object representing the product_div.

    Returns:
        Product: The created Product object.

    """
    name = product_div.find("span", {"class": "product-name"}).find("a").text.strip()
    price = product_div.find("span", {"class": "price"}).text.strip()
    sku = product_div.find("span", {"class": "product-sku"}).text.strip()
    product_url = product_div.find("span", {"class": "product-name"}).find("a")["href"]
    return Product(name, price, sku, product_url)


def scrape_data_from_link(url: str, pbar: tqdm) -> dict[str, Product]:
    """
    Scrapes data from a given URL and returns a dictionary of products.

    Args:
        url (str): The URL to scrape data from.
        pbar (tqdm): The progress bar object to update.

    Returns:
        dict[str, Product]: A dictionary containing the scraped product data.
    """
    all_data = {}
    base_url = url
    page_product_info = {}
    total_pages = get_total_pages(base_url)

    print(f"Scraping data from {base_url}")
    print(f"Total pages: {total_pages}")

    for page_number in range(1, total_pages + 1):
        paginated_url = f"{base_url}?p={page_number}&product_list_limit={MAX_PRODUCTS_PER_PAGE}"
        response = requests.get(paginated_url)

        if response.status_code != 200:
            print(f"Failed to get data from {paginated_url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for product_div in soup.find_all("div", {"class": "product-item-info"}):
            product = create_product_from_div(product_div)
            page_product_info[product.name] = product

        all_data.update(page_product_info)
        pbar.update()

    return all_data


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
    """
    Main function to scrape data from links and save it to a JSON file.
    """
    # Load links from file
    try:
        with open("src/links.txt", "r") as f:
            links = [line.strip() for line in f]
    except FileNotFoundError:
        print("Could not find the links file.")
        return

    # Get the total number of pages for each link to allow tqdm to be used
    pages_count = sum(get_total_pages(link) for link in links)

    # Scrape data from each link
    all_data = {}
    with tqdm(total=pages_count) as pbar:
        for link in links:
            data = scrape_data_from_link(link, pbar)
            all_data.update(data)

    # Save data to file at the very end
    try:
        with open("data/scraped_data.json", "w") as f:
            json.dump(all_data, f, indent=2)
    except IOError:
        print("Could not write to the output file.")


if __name__ == "__main__":
    main()
