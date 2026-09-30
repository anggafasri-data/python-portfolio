# IMDb Advanced Search Scraper

## Overview

A robust web scraping pipeline built to extract movie metadata from IMDb's Advanced Search platform. It bypasses strict anti-bot protections, handles dynamic React-based UI elements, and overcomes lazy-loading pagination to extract large-scale datasets.

## Technologies Used

- Python
- Selenium
- Undetected-Chromedriver
- BeautifulSoup4
- Pandas

## Key Features

- **Anti-Bot Bypass:** Utilizes undetected-chromedriver to navigate security blocks.
- **Dynamic Interaction:** Automates dropdown selection and custom JavaScript clicks.
- **Lazy Loading Handling:** Programmatically scrolls to reveal hidden elements, extracting 1,000+ records.

## Extracted Data Points

1. Movie Title
2. Release Year
3. Duration
4. IMDb Rating

## Project Structure

```text
imdb-scraper-selenium-beautifulsoup/
│
├── data/
│   └── imdb_advanced_search_results.xlsx   # The final extracted dataset
│
├── screenshots/
│   └── image.png           # Visual output / result screenshot
│
├── imdb_scraper.ipynb                      # Main Jupyter Notebook containing the scraper logic
└── README.md
```

## Author

**Angga Fasri Nur**
