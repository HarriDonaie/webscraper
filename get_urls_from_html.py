from bs4 import BeautifulSoup as bs
import urllib.parse

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

# test_string = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><br /><a href="https://home.donaie.uk"><span>Harri Home</span></a></body></html>'
# test_string2 = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><br /><a href="/porno.py"><span>Harri Home</span></a></body></html>'

# get_urls_from_html(test_string, "")
# get_urls_from_html(test_string2, "https://crawler-test.com")