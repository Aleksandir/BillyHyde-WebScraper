import requests
from bs4 import BeautifulSoup


def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # This list comprehension extracts all the href attributes from anchor tags (a) with class "nav-anchor" and data-color "#ffffff"
    # It only includes those hrefs that start with "http", indicating they are complete URLs
    links = [
        link.get("href")
        for link in soup.find_all("a", {"class": "nav-anchor", "data-color": "#ffffff"})
        if link.get("href", "").startswith("http")
    ]

    return links


def save_links(links, file_path):
    with open(file_path, "w") as file:
        for link in links:
            file.write(f"{link}\n")


def main():
    url = "https://billyhydemusic.com.au"  # Replace with your target URL
    links = scrape_links(url)
    save_links(links, "src/links.txt")


if __name__ == "__main__":
    main()
