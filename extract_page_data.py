from get_urls_from_html import get_urls_from_html, get_images_from_html
from get_first_paragraph_from_html import get_first_paragraph_from_html
from get_heading_from_html import get_heading_from_html
from crawl import normalize_url
from typing import TypedDict


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