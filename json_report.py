import json

def write_json_report(page_data, filename="report.json") -> None:
    page_list = sorted(page_data.values(), key = lambda p: p["url"])

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(page_list, file, indent = 2)