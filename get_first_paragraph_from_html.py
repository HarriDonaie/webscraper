from bs4 import BeautifulSoup as bs, Tag


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