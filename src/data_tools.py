import json
import pprint

with open("data/scraped_data.json", "r") as f:
    data = json.load(f)

max_price = 0
max_product = None

for name, product in data.items():
    if float(product["price"].strip("$").replace(",", "")) > float(max_price):
        max_price = product["price"].strip("$").replace(",", "")
        max_product = product

print(pprint.pformat(max_product))
# print(name, product)
