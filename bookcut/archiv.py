from bs4 import BeautifulSoup as soup
import requests
from bookcut.mirror_checker import pageStatus

ARCHIV_URL = 'http://export.arxiv.org/'
ARCHIV_SEARCH_URL = ("http://search.arxiv.org:8081/?query={}&in=")

def archiv(book, author):
    status = pageStatus(ARCHIV_URL)
    if status:
        book = book.split(' ')
        title_term = ''
        for i in book:
            title_term = title_term + "+" + i
        author_term = ''
        if ' ' in author:
            author = author.split(' ')
            for i in author:
                author_term = author_term + " +" + i


        fullterm = author_term + title_term
        search_url = ARCHIV_SEARCH_URL.format(fullterm)
        req = requests.get(search_url)
        search_page_html = soup(req.content, 'html.parser')
        print(search_url)

if __name__ == '__main__':
    archiv("Physics of the Bacon Internal Resonator Banjo", 'David Politzer')
