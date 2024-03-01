from unittest.mock import AsyncMock, patch

import pytest

from scraper import FreeImagesAsyncScraper


@pytest.fixture
def html_content():
    return """<html>
                <body>
                    <article class="grid-article"><a class="grid-link" href="/photo/dog-1383342"> <figure class="grid-figure" style="background:#fff"><picture><source srcset="https://images.freeimages.com/images/large-previews/3f8/dog-1383342.jpg?fmt=webp&amp;w=500"><img alt="dog" class="grid-thumb" height="1600" loading="lazy" src="https://images.freeimages.com/images/large-previews/3f8/dog-1383342.jpg?fmt=webp&amp;w=500" width="2000"></picture><figcaption class="figcaption">cuteeeeyy</figcaption></figure> </a><div class="grid-item-overlay absolute z-10 opacity-0 top-0 left-0 right-0 bottom-0 pointer-events-none transition-opacity"><div class="flex flex-col justify-between group absolute w-full h-full"><div class="thumb-overlay-container flex h-full w-full"><div class="w-full h-full bg-gradient-to-t from-black-op-0.6 to-transparent relative"><div class="tags-container absolute px-4 py-3"><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/dog"> dog </a><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/dogg"> dogg </a><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/doggy"> doggy </a></div><div class="flex h-full items-end px-4 py-3"><h4 class="text-white truncate">Dog</h4></div></div></div></div></div></article>
                    <article class="grid-article"><a class="grid-link" href="/photo/dog-1383342"> <figure class="grid-figure" style="background:#fff"><picture><source srcset="https://images.freeimages.com/images/large-previews/3f8/dog-1383342.jpg?fmt=webp&amp;w=500"><img alt="dog" class="grid-thumb" height="1600" loading="lazy" src="https://images.freeimages.com/images/large-previews/3f8/dog-1383342.jpg?fmt=webp&amp;w=500" width="2000"></picture><figcaption class="figcaption">cuteeeeyy</figcaption></figure> </a><div class="grid-item-overlay absolute z-10 opacity-0 top-0 left-0 right-0 bottom-0 pointer-events-none transition-opacity"><div class="flex flex-col justify-between group absolute w-full h-full"><div class="thumb-overlay-container flex h-full w-full"><div class="w-full h-full bg-gradient-to-t from-black-op-0.6 to-transparent relative"><div class="tags-container absolute px-4 py-3"><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/dog"> dog </a><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/dogg"> dogg </a><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/doggy"> doggy </a></div><div class="flex h-full items-end px-4 py-3"><h4 class="text-white truncate">Dog</h4></div></div></div></div></div></article>
                    <article class="grid-article"><a class="grid-link" href="/photo/dog-1383342"> <figure class="grid-figure" style="background:#fff"><picture><source srcset="https://images.freeimages.com/images/large-previews/3f8/dog-1383342.jpg?fmt=webp&amp;w=500"><img alt="dog" class="grid-thumb" height="1600" loading="lazy" src="https://images.freeimages.com/images/large-previews/3f8/dog-1383342.jpg?fmt=webp&amp;w=500" width="2000"></picture><figcaption class="figcaption">cuteeeeyy</figcaption></figure> </a><div class="grid-item-overlay absolute z-10 opacity-0 top-0 left-0 right-0 bottom-0 pointer-events-none transition-opacity"><div class="flex flex-col justify-between group absolute w-full h-full"><div class="thumb-overlay-container flex h-full w-full"><div class="w-full h-full bg-gradient-to-t from-black-op-0.6 to-transparent relative"><div class="tags-container absolute px-4 py-3"><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/dog"> dog </a><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/dogg"> dogg </a><a class="bg-opacity-20 bg-black px-2.5 py-1 rounded-full text-sm text-white mb-0.5 inline-block backdrop-filter backdrop-blur-sm pointer-events-auto" href="/search/doggy"> doggy </a></div><div class="flex h-full items-end px-4 py-3"><h4 class="text-white truncate">Dog</h4></div></div></div></div></div></article>
                </body>
    </html>
"""


@pytest.fixture
@patch("writers.FileWriter")
def async_scraper(mocked_writer):
    mocked_async_scraper = FreeImagesAsyncScraper(
        number_of_items=60, query="dog", writer=mocked_writer
    )
    return mocked_async_scraper


def test_parse(async_scraper, html_content):
    # Parses the HTML fixture
    scraper = async_scraper.parse(html_content)

    # asserts that get 3 elements out of the html (the three articles)
    assert len(scraper) == 3


def test_parse_no_content(async_scraper):
    # parses an empty html
    scraper = async_scraper.parse("")

    # asserts that gets no elements.
    assert len(scraper) == 0


@patch("scraper.FreeImagesAsyncScraper.parse")
@patch("scraper.FreeImagesAsyncScraper.fetch")
@pytest.mark.asyncio
async def test_scrape_page(mocked_fetch, mocked_parse, async_scraper, html_content):
    # mocks the fetch function to return the mocked html
    mocked_fetch.return_value = html_content

    # the parse function will return 3 random elements.
    mocked_parse.return_value = [1, 2, 3]

    # calls the scrape page function for the first page
    res = await async_scraper.scrape_page(1)

    # asserts that the website called is the first page
    mocked_fetch.assert_called_once_with(
        f"{async_scraper.BASE_URL}/search/{async_scraper.query}/1"
    )

    # asserts that the parse function was called once with the mocked html.
    mocked_parse.assert_called_once_with(html_content)

    # the len of the response must be 3 (quantity of elements after parsing the html)
    assert len(res) == 3


@patch("scraper.FreeImagesAsyncScraper.parse")
@patch("scraper.FreeImagesAsyncScraper.fetch")
@pytest.mark.asyncio
async def test_scrape_page_no_content(mocked_fetch, mocked_parse, async_scraper):
    # mocks fetch and parse return values. In this case, the content is empty
    mocked_fetch.return_value = ""
    mocked_parse.return_value = []

    # calls scrape page to scrape the first page.
    res = await async_scraper.scrape_page(1)

    # asserts that the first page was called.
    mocked_fetch.assert_called_once_with(
        f"{async_scraper.BASE_URL}/search/{async_scraper.query}/1"
    )

    # Since the html is empty, it calls the parse without any content.
    mocked_parse.assert_called_once_with("")

    # asserts that the len of the response is 0, which means that it didn't get any images.
    assert len(res) == 0


@patch("scraper.FreeImagesAsyncScraper.scrape_page")
@pytest.mark.asyncio
async def test_generate_tasks(mocked_scrape_page, async_scraper):
    # mocks the scrape page function.
    mocked_scrape_page.side_effect = lambda x: [f"Page {x}"]

    # generate the tasks.
    tasks = async_scraper.generate_tasks()

    # assert that the len of the tasks equals the max pages. It calculates the ceil(number_of_items / self.ITEMS_PER_PAGE).
    assert len(tasks) == async_scraper.max_pages

    # for each task, it asserts that the scrape page returns the correct page which was mocked above.
    for i, task in enumerate(tasks, start=1):
        assert await task == [f"Page {i}"]


@patch("scraper.FreeImagesAsyncScraper.write_to_storage")
@pytest.mark.asyncio
async def test_process_tasks_in_chunks(mocked_write_to_storage, async_scraper):
    # generate a list of AsyncMocks representing asynchronous coroutines
    coro_results = [AsyncMock(return_value=f"test_{_}") for _ in range(1, 5)]

    # mock the asyncio.gather function to simulate asynchronous task execution
    with patch("asyncio.gather", AsyncMock()) as mocked_gather:
        # define a test list containing task results to be returned by asyncio.gather
        test_list = ["test_1", "test_2", "test_3", "test_4", "test_5"]
        mocked_gather.return_value = [test_list]

        # call the function under test and store the result
        result = await async_scraper.process_tasks_in_chunks(coro_results)

    # the write_to_storage function is called exactly once
    assert mocked_write_to_storage.call_count == 1

    # the result matches the expected len of 5
    assert result == 5
