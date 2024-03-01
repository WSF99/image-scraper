# Free Images Scraper

## Overview
This Python program is designed to scrape images from the [Free Images](https://www.freeimages.com/) website. It utilizes asynchronous programming with the `aiohttp` library for efficient web scraping. The scraped data is then processed, and the relevant information is saved into a specified storage.

## Features
- Asynchronous Scraping: The program uses asynchronous programming to concurrently scrape multiple pages, enhancing efficiency.
- Chunked Processing: Results from scraped pages are processed in chunks, optimizing memory usage.

## Installation
1. Clone the repository
    ```bash
    git clone https://github.com/WSF99/image-scraper.git
    ```
2. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the scraper with
    ```bash
    python main.py
    ```
2. The scraped images will be stored in a local storage (`SQLite`)

## Testing

For testing purposes, run the following command using `pytest`:
```bash
pytest .
```

## Performance
The Free Images Scraper is optimized for speed, allowing you to scrape a large number of images efficiently. Here are some performance metrics based on a quick test:
- Scraped Images: 6000
- Number of Pages: 100
- Scraping Time: ~7 seconds

Please note that the actual scraping speed may vary based on factors such as network conditions and system resources.

## Estimated Scraping Rate
Based on the provided metrics, the estimated scraping rate is:

- Pages per Second: 14.29 pages/second
- Pages per Minute: 857 pages/minute
- Pages per Hour: 51420 pages/hour
