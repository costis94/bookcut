from bs4 import BeautifulSoup as soup
import requests
import mechanize
from bookcut.mirror_checker import pageStatus, main as mirror_checker
import pandas as pd

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
        print(len(titles), len(book_urls))
        arxiv_df = pd.DataFrame({'Title': titles, 'Url': book_urls})
        return arxiv_df


def libgen_repo(term):
    url = mirror_checker()
    if url is not None:
        br = mechanize.Browser()
        br.set_handle_robots(False)   # ignore robots
        br.set_handle_refresh(False)  #
        br.addheaders = [('User-agent', 'Firefox')]

        br.open(url)
        br.select_form('libgen')
        input_form = term
        br.form['req'] = input_form
        ac = br.submit()
        html_from_page = ac
        html_soup = soup(html_from_page,'html.parser')
        table = html_soup.find_all('table')[2]

        table_data = []
        mirrors = []
        extensions = []

        for i in table:
            j = 0
            try:
                td = i.find_all('td')
                for tr in td:
                    # scrape mirror links
                    if j == 9:
                        temp = tr.find('a', href=True)
                        mirrors.append(temp['href'])
                    j = j + 1
                row = [tr.text for tr in td]
                table_data.append(row)
                extensions.append(row[8])

            except:
                pass

        # Clean result page
        for j in table_data:
            j.pop(0)
            del j[8:15]
        headers = ['Author(s)', 'Title', 'Publisher', 'Year', 'Pages',
                   'Language', 'Size', 'Extension']


        tabular = pd.DataFrame(table_data)
        tabular.columns = headers
        tabular['Url'] = mirrors
        return tabular
