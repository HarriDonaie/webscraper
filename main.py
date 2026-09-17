from urllib.parse import urlsplit
from bs4 import BeautifulSoup as bs
import urllib.parse
#from extract_page_data import extract_page_data
#from get_urls_from_html import get_urls_from_html, get_images_from_html
#from get_first_paragraph_from_html import get_first_paragraph_from_html
#from get_heading_from_html import get_heading_from_html
import sys
from typing import TypedDict
import pprint, asyncio, aiohttp

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def extract_page_data(html: str, page_url: str) ->  PageData:
    page_data: PageData = {
        "url": "https://" + normalize_url(page_url),
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }

    return page_data

def get_urls_from_html(html, base_url):
    html_file = bs(html, "html.parser")
    try:
        all_anchors = html_file.find_all("a")
        all_urls = [urllib.parse.urljoin(base_url, anchor.get("href")) for anchor in all_anchors]
    except:
        raise Exception("No links found in html text")

    #print(all_urls)
    return all_urls

def get_images_from_html(html, base_url):
    html_file = bs(html, "html.parser")
    try:
        all_anchors = html_file.find_all("img")
        all_images = [urllib.parse.urljoin(base_url, anchor.get("src")) for anchor in all_anchors]
    except:
        raise Exception("No images found in html text")

    #print(all_images)
    return all_images

def get_first_paragraph_from_html(html: str) -> str:
    html_file = bs(html, "html.parser")
    # print(type(html))
    # print(type(html_file))
    # print(type(html_file.find("main").get_text()))
    main_body = html_file.find("main")
    # print(type(main_body))
    # print(main_body)
    try:
        if main_body.find("p") is not None:
            first_paragraph = main_body.find("p").get_text()
        else: 
            first_paragraph = ""
        return first_paragraph
    except AttributeError:
        if html_file.find("p") is not None:
            first_paragraph = html_file.find("p").get_text()
        else: 
            first_paragraph = ""
        return first_paragraph

def get_heading_from_html(html: str) -> str:
    html_file = bs(html, "html.parser")
    

    if html_file.find("h1") is not None:
        heading_line = html_file.find("h1").get_text()
    elif html_file.find("h2") is not None:
        heading_line = html_file.find("h2").get_text()
    else: 
        heading_line = ""
    return heading_line

def normalize_url(url: str) -> str:
    parsed_url = urlsplit(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()

# def get_html(url: str) -> str:
#     try:
#         html = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
#         if html.status_code >= 400:
#             raise Exception(f"HTTP error {html.status_code}")
#         if not "text/html" in html.headers["content-type"]:
#             raise Exception(f"Error: Response content is not text: {html.headers["content-type"]}")
#     except Exception as e:
#         raise Exception(f"Another error has occurred parsing url {url}: {e}")
#     return html.text

class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int = 3, max_pages: int = 10):
        self.base_url = base_url
        self.base_domain = urlsplit(self.base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock: asyncio.Lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession = None
        self.should_stop = False
        self.all_tasks: set = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalised_url):
        async with self.lock:
            if self.should_stop == True:
                return False
            if normalised_url in self.visited:
                            return False
            if len(self.visited) == self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False
            self.visited.add(normalised_url)
            return True

    async def get_html(self, url: str) -> str:
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            try:
                if response.status >= 400:
                    raise Exception(f"HTTP error {response.status}")
                content_type = response.headers.get("content-type", "")
                if not "text/html" in content_type:
                    raise Exception(f"Error: Response content is not text: {content_type}")
            except Exception as e:
                raise Exception(f"Another error has occurred parsing url {url}: {e}")
            return await response.text()
        

    async def crawl_page(self, base_url, current_url = None):
        # if self.should_stop == True:
        #     return
        if current_url == None:
            current_url = base_url
        if not urllib.parse.urlparse(base_url).netloc == urllib.parse.urlparse(current_url).netloc:
            return 

        current_url_normal = normalize_url(current_url)

        if not await self.add_page_visit(current_url_normal):
            return

        
        async with self.semaphore:
            print(f"Crawling page: {current_url_normal} (Active: {self.max_concurrency - self.semaphore._value})")
            html = await self.get_html(current_url)
        if self.should_stop:
            return
        current_url_html = extract_page_data(html, current_url)
        async with self.lock:
            # print(self.page_data)
            self.page_data[current_url_normal] = current_url_html
        tasks = []
        for link in self.page_data[current_url_normal]["outgoing_links"]:
            task = asyncio.create_task(self.crawl_page(base_url, link))
            self.all_tasks.add(task)
            tasks.append(task)
        try:
            await asyncio.gather(*tasks)
        finally:
            for task in tasks:
                self.all_tasks.discard(task)
        


        # if current_url_normal in page_data.keys():
        #     return

        # current_url_html = get_html(current_url)
        # print(f"Now crawling: {current_url_normal}")

        # page_data[current_url_normal] = extract_page_data(current_url_html, current_url)

        # for link in page_data[current_url_normal]["outgoing_links"]:
        #     crawl_page(base_url, link, page_data)

        # return page_data

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(url, max_concurrency, max_pages) -> dict:
    async with AsyncCrawler(url, max_concurrency, max_pages) as crawler:
        data_dict = await crawler.crawl()
        return data_dict


async def main(args = sys.argv):
    if len(args) < 2:
        print("no website provided")
        exit(1)
    elif len(args) > 4:
        print("too many arguments provided")
        exit(1)
    BASE_URL = args[1]
    MAX_CONCUR = int(args[2])
    MAX_PAGES = int(args[3])
    print(f"starting crawl of: {BASE_URL}")
    page_data = await crawl_site_async(BASE_URL, MAX_CONCUR, MAX_PAGES)
    print(f"----- Crawl complete. -----\nPages found: {len(page_data)}\n-----\nList of pages found:")
    for link, info in page_data.items():
        print(info["url"])
    print(f"\nInformation for the last page crawled:")
    pprint.pprint(next(reversed(page_data.items())))

if __name__ == "__main__":
    asyncio.run(main())