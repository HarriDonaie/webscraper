from bs4 import BeautifulSoup as bs, Tag


def get_heading_from_html(html: str) -> str:
    html_file = bs(html, "html.parser")
    

    if html_file.find("h1") is not None:
        heading_line = html_file.find("h1").get_text()
    elif html_file.find("h2") is not None:
        heading_line = html_file.find("h2").get_text()
    else: 
        heading_line = ""
    return heading_line