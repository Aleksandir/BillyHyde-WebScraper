import requests
from bs4 import BeautifulSoup


def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for link in soup.find_all("a", {"class": "nav-anchor", "data-color": "#ffffff"}):
        href = link.get("href")
        print(href)
        if href and href.startswith("http"):
            links.append(href)

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
