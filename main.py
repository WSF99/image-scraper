import asyncio
from time import time

from scraper import FreeImagesAsyncScraper
from writers import DatabaseWriter


async def main():
    start = time()

    use_default_values = (
        input("Do you want to use default values? (y/n): ").lower() == "y"
    )

    if use_default_values:
        number_of_items = 1000
        query = "dog"
    else:
        number_of_items = int(input("Enter the number of images: "))
        query = input("Enter the query: ")

    writer = DatabaseWriter()
    scraper = FreeImagesAsyncScraper(number_of_items, query, writer)

    print(f"Running scraper on {number_of_items} items. Query: {query}")

    items_scraped = await scraper.scrap()
    time_elapsed = f"{time() - start:.2f}"

    table_name = writer.table_name

    print(
        f"Successfully scraped and saved {items_scraped} images into the '{table_name}' table. Time elapsed: {time_elapsed}s"
    )


if __name__ == "__main__":
    asyncio.run(main())
