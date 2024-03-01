import asyncio
from math import ceil
from typing import Any, Coroutine, Union

import aiohttp
from bs4 import BeautifulSoup

from helpers import chunks
from writers import IWriter


class FreeImagesAsyncScraper:
    BASE_URL = "https://www.freeimages.com"
    ITEMS_PER_PAGE = 60

    def __init__(
        self,
        number_of_items: int,
        query: str,
        writer: IWriter,
        chunk_size: int = 25,
    ):
        # Number of items to scrap.
        self.number_of_items = number_of_items

        # Query for finding the images.
        self.query = query

        # Writer responsible for saving in the specified storage.
        self.writer = writer

        # The Chunk Size defines how many concurrent pages will be processed during the Scrap process.
        self.chunk_size = chunk_size

        # The max pages is defined by the ceiling of the number of items divided by the items per page.
        # The items per page in the free images website is 60. So we always divide by that number.
        self.max_pages = ceil(number_of_items / self.ITEMS_PER_PAGE)

    @staticmethod
    async def fetch(url: str) -> Coroutine[Any, Any, str]:
        """
        Asynchronously fetch data from a given URL using an aiohttp ClientSession.

        This method sends an HTTP GET request to the specified URL and returns the response text.

        Parameters
        ----------
        url : str
            The URL for the HTTP GET request.

        Returns
        -------
        Coroutine[Any, Any, str]
            A coroutine representing the response text.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.text()
        except aiohttp.ClientError as ce:
            print(f"An error occurred during the HTTP request: {ce}")

    def parse(self, html_content: str) -> Union[list[str], list]:
        """
        Parse the data.

        This function is responsible for parsing the HTML content and extracting relevant information.

        Parameters
        ----------
        html_content : str
            The HTML content to be parsed.

        Returns
        -------
        Union[list[str], list]
            A list of dictionaries containing parsed data. Each dictionary has a key 'address' representing a parsed link.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        urls = [
            a["href"]
            for a in soup.select("article.grid-article a.grid-link[href]")
            if a.get("href")
        ]

        return [self.BASE_URL + url for url in urls]

    async def scrape_page(self, page: int) -> Coroutine[Any, Any, list[str] | list]:
        """
        Asynchronously scrape and parse a specific page of search results.

        This method constructs the URL for the specified page, fetches the HTML content,
        and then parses the content to extract relevant information.

        Parameters
        ----------
        page : int
            The page number to scrape.

        Returns
        -------
        Coroutine[Any, Any, list[str] | list]
            If successful, returns a list of dictionaries containing parsed information
            from the page.
        """
        url = f"{self.BASE_URL}/search/{self.query}/{page}"
        html_content = await self.fetch(url)
        print(f"Successfully scraped page {page}.")
        return self.parse(html_content)

    def write_to_storage(self, task: Union[list[str], list]) -> None:
        """
        Write a list of URLs to the storage.

        Parameters
        ----------
        task : Union[list[str], list]
            A list containing URLs to be written to the storage. Typically, each task
            represents a batch of URLs, often with a size of 60.

        Returns
        -------
        None
            This method does not return any value.

        """
        self.writer.write(task)

    def generate_tasks(
        self,
    ) -> list[Coroutine[Any, Any, Coroutine[Any, Any, list[str] | list]]]:
        """
        Generate a list of coroutines representing tasks to scrape pages.

        Returns
        -------
        list[Coroutine[Any, Any, Coroutine[Any, Any, list[str] | list]]]
            A list of coroutines, each representing a task to scrape a specific page.

        Notes
        -----
        This method creates a list of coroutines by invoking the `scrape_page` coroutine
        for each page within the specified range. These coroutines collectively represent
        the tasks for scraping multiple pages.
        """
        tasks = [self.scrape_page(page) for page in range(1, self.max_pages + 1)]
        return tasks

    async def process_tasks_in_chunks(
        self, tasks: list[Coroutine[Any, Any, Coroutine[Any, Any, list[str] | list]]]
    ) -> int:
        """
        Asynchronously process and write tasks in chunks to the storage.

        Parameters
        ----------
        tasks : list[Coroutine[Any, Any, Coroutine[Any, Any, list[str] | list]]]
            A list of coroutines, each representing a task.

        Returns
        -------
        int
            The total count of processed items.

        Notes
        -----
        This method asynchronously processes tasks in chunks, where each chunk is a subset of
        the provided tasks. It writes the processed data to the storage, ensuring that the
        order is maintained. The total count of processed items is returned.
        """
        processed_items_count = 0
        for chunk in chunks(tasks, self.chunk_size):
            processed_tasks = await asyncio.gather(*chunk)
            for task in processed_tasks:
                data = (
                    task
                    if processed_items_count + len(task) <= self.number_of_items
                    else task[: self.number_of_items - processed_items_count]
                )
                self.write_to_storage(data)
                processed_items_count += len(data)

                if processed_items_count >= self.number_of_items:
                    break

        return processed_items_count

    async def scrap(self):
        """
        Asynchronously initiate the scraping process.

        Returns
        -------
        int
            The total count of processed items during the scraping process.

        Notes
        -----
        This method orchestrates the scraping process by generating tasks and processing them
        in chunks using asyncio. It returns the total count of processed items.
        """
        tasks = self.generate_tasks()

        processed_items_count = await self.process_tasks_in_chunks(tasks)

        return processed_items_count
