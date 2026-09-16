from bs4 import BeautifulSoup as bs, Tag


def get_heading_from_html(html: str) -> str:
    html_file = bs(html, "html.parser")
    heading_line = ""
    try:
        if html_file.find("<h1>") is not None:
            heading_line = html_file.find("<h1>")
    except:
        try:
            if html_file.find("<h2>") is not None:
                heading_line = html_file.find("<h2>")
        except: 
            return ""
    print(heading_line)
    return heading_line[4:-5]

