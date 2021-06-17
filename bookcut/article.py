from bookcut.repositories import open_access_button
from bookcut.downloader import filename_refubrished
from bookcut.search import search_downloader
from click import confirm

"""
Article.py is using from article command and searches repositories for
published articles.
"""


def article_search(doi, title):
    try:
        article_json_data = open_access_button(doi, title)
        url = article_json_data["url"]
        metadata = article_json_data["metadata"]
        title = metadata["title"]
        filename = filename_refubrished(title)
        filename = filename + ".pdf"
        ask_for_downloading(filename, url)
    except KeyError:
        print("\nCan not find the given article.\nPlease try another search!")


def ask_for_downloading(articlefilename, url):
    ask = confirm(f"Do you want to download:\n {articlefilename}")
    if ask is True:
        search_downloader(articlefilename, url)
    else:
        print("Aborted!")
