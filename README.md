# BillyHyde Web Scraping Project

This project contains two Python scripts for web scraping. The first script, `link_scraper.py`, scrapes links from a target website and saves them into a text file. The second script, `data_scraper.py`, reads the links from the text file, visits each link, and scrapes the data from the linked pages. The scraped data is then saved in JSON format.

## Setup

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Run the `link_scraper.py` script to scrape links from the target website:

```
python src/link_scraper.py
```

This will create a `links.txt` file in the `src` directory.

2. Run the `data_scraper.py` script to scrape data from the linked pages:

```
python src/data_scraper.py
```

This will create a `scraped_data.json` file in the `data` directory.

3. Use the `data_tools.py` script to analyze and present information about the scraped data:

```
python src/data_tools.py
```

This script reads the `scraped_data.json` file from the `data` directory and provides various insights about the data, such as the product with the highest price.
