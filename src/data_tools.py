import json
import pprint


def max_price():
    with open("data/scraped_data.json", "r") as f:
        data = json.load(f)

    max_price = 0
    max_product = None

    for _, product in data.items():
        if float(product["price"].strip("$").replace(",", "")) > float(max_price):
            max_price = product["price"].strip("$").replace(",", "")
            max_product = product

    return max_product


def min_price():
    with open("data/scraped_data.json", "r") as f:
        data = json.load(f)

    min_price = 99
    min_product = None

    for _, product in data.items():
        if float(product["price"].strip("$").replace(",", "")) < float(min_price):
            min_price = product["price"].strip("$").replace(",", "")
            min_product = product

    return min_product


def total_number_of_products():
    with open("data/scraped_data.json", "r") as f:
        data = json.load(f)

    return len(data)


def average_price():
    with open("data/scraped_data.json", "r") as f:
        data = json.load(f)

    total_price = 0

    for _, product in data.items():
        total_price += float(product["price"].strip("$").replace(",", ""))

    return round(total_price / len(data), 2)


def main():
    # pretty print does not work with newlines, used print instead, continued for consistency
    pprint.pprint(f"highest price product: {max_price()}")
    print()
    pprint.pprint(f"lowest price product: {min_price()}")
    print()
    print(f"total number of products: {total_number_of_products()}")
    print()
    print(f"Average price: ${average_price()}")


if __name__ == "__main__":
    main()
