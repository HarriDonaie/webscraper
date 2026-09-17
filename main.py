from urllib.parse import urlsplit
from bs4 import BeautifulSoup as bs
import urllib.parse
#from extract_page_data import extract_page_data
#from get_urls_from_html import get_urls_from_html, get_images_from_html
#from get_first_paragraph_from_html import get_first_paragraph_from_html
#from get_heading_from_html import get_heading_from_html
import sys
from typing import TypedDict
import requests, pprint

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

def get_html(url: str) -> str:
    try:
        html = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
        if html.status_code >= 400:
            raise Exception(f"HTTP error {html.status_code}")
        if not "text/html" in html.headers["content-type"]:
            raise Exception(f"Error: Response content is not text: {html.headers["content-type"]}")
    except:
        raise Exception("Other error has occurred")
    return html.text

def crawl_page(base_url, current_url = None, page_data = None):
    if current_url == None:
        current_url = base_url
    if page_data == None:
        page_data = {}
    if not urllib.parse.urlparse(base_url).netloc == urllib.parse.urlparse(current_url).netloc:
        return 

    current_url_normal = normalize_url(current_url)

    if current_url_normal in page_data.keys():
        return

    current_url_html = get_html(current_url)
    print(f"Now crawling: {current_url_normal}")

    page_data[current_url_normal] = extract_page_data(current_url_html, current_url)

    for link in page_data[current_url_normal]["outgoing_links"]:
        crawl_page(base_url, link, page_data)

    return page_data



def main(args = sys.argv):
    if len(args) < 2:
        print("no website provided")
        exit(1)
    elif len(args) > 2:
        print("too many arguments provided")
        exit(1)
    BASE_URL = args[1]
    print(f"starting crawl of: {BASE_URL}")
    html = crawl_page(BASE_URL)
    print(f"Crawl complete.\nPages found: {len(html)}\nList of pages found:")
    # for link, info in html.items():
    #     print(info["url"])
    print(f"\nInformation for the last page crawled:")
    pprint.pprint(next(reversed(html.items())))

main()