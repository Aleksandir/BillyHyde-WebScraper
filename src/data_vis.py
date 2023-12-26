import json

import matplotlib.pyplot as plt


class DataAnalyzer:
    """
    A class for analyzing data from a JSON file.

    Args:
        data_file (str): The path to the JSON file containing the data.

    Attributes:
        data (dict): The loaded data from the JSON file.

    Methods:
        max_price: Returns the product with the maximum price.
        min_price: Returns the product with the minimum price.
        total_number_of_products: Returns the total number of products.
        average_price: Returns the average price of all products.
        plot_prices: Plots a scatter plot of product prices.

    """

    def __init__(self, data_file):
        with open(data_file, "r") as f:
            self.data = json.load(f)

    def max_price(self):
        """
        Returns the product with the maximum price.

        Returns:
            dict: The product with the maximum price.

        """
        with open("data/scraped_data.json", "r") as f:
            data = json.load(f)

        max_price = 0
        max_product = None

        for _, product in data.items():
            if float(product["price"].strip("$").replace(",", "")) > float(max_price):
                max_price = product["price"].strip("$").replace(",", "")
                max_product = product

        return max_product

    def min_price(self):
        """
        Returns the product with the minimum price.

        Returns:
            dict: The product with the minimum price.

        """
        with open("data/scraped_data.json", "r") as f:
            data = json.load(f)

        min_price = 99
        min_product = None

        for _, product in data.items():
            if float(product["price"].strip("$").replace(",", "")) < float(min_price):
                min_price = product["price"].strip("$").replace(",", "")
                min_product = product

        return min_product

    def total_number_of_products(self):
        """
        Returns the total number of products.

        Returns:
            int: The total number of products.

        """
        return len(self.data)

    def average_price(self):
        """
        Returns the average price of all products.

        Returns:
            float: The average price.

        """
        with open("data/scraped_data.json", "r") as f:
            data = json.load(f)

        total_price = 0

        for _, product in data.items():
            total_price += float(product["price"].strip("$").replace(",", ""))

        return round(total_price / len(data), 2)

    def plot_prices(self):
        """
        Plots a scatter plot of product prices.

        """
        with open("data/scraped_data.json", "r") as f:
            data = json.load(f)

        prices = []
        for _, product in data.items():
            prices.append(float(product["price"].strip("$").replace(",", "")))

        average = self.average_price()

        plt.figure(figsize=(10, 6))  # Adjust the width and height as needed
        plt.scatter(range(len(prices)), prices)
        plt.axhline(y=average, color="r", linestyle="--")
        plt.xlabel("Product")
        plt.ylabel("Price")
        plt.title("Product Prices")
        plt.text(0, average, f"Average Price: ${average}", ha="center", va="bottom", color="r")
        plt.show()


def main():
    analyzer = DataAnalyzer("data/scraped_data.json")
    max_product = analyzer.max_price()
    min_product = analyzer.min_price()
    total_products = analyzer.total_number_of_products()
    average_price = analyzer.average_price()

    print("Product with Maximum Price:")
    print(max_product)
    print()

    print("Product with Minimum Price:")
    print(min_product)
    print()

    print("Total Number of Products:")
    print(total_products)
    print()

    print("Average Price:")
    print(average_price)
    print()

    analyzer.plot_prices()


if __name__ == "__main__":
    main()
