from bs4 import BeautifulSoup as soup
import requests
from bookcut.mirror_checker import pageStatus

ARCHIV_URL = 'http://export.arxiv.org/'
ARCHIV_SEARCH_URL = ("http://search.arxiv.org:8081/?query={}&in=")

def arxiv(book, author):
    status = pageStatus(ARCHIV_URL)
    if status:
        # preparing search term for url
        book = book.split(' ')
        title_term = ''
        for i in book:
            title_term = title_term + "+" + i
        author_term = ''
        if ' ' in author:
            author = author.split(' ')
            for i in author:
                author_term = author_term + "+" + i
        fullterm = author_term + title_term
        fullterm = fullterm.strip(' ')
        search_url = ARCHIV_SEARCH_URL.format(fullterm)  # search page url

        # parsing page data
        req = requests.get(search_url)
        search_page_html = soup(req.content, 'html.parser')
        # extracting and preparing book title results
        raw_titles = search_page_html.findAll('span', {'class': 'title'})
        titles = []
        for i in raw_titles:
            titles.append(i.text)
        # extracting and preparing book urls
        raw_urls = search_page_html.findAll('td', {'class': 'snipp'})
        book_urls = []
        for i in raw_urls:
            s = i.find('a')
            book_urls.append('http://search.arxiv.org:8081/'+s['href'])
        arxiv_data = dict(zip(titles,book_urls))
        return arxiv_data
