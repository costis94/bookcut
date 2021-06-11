from bookcut.mirror_checker import settingParser
import mechanize
from bs4 import BeautifulSoup as Soup
from bookcut.libgen import file_name
from click import confirm
from bookcut.downloader import downloading
from bookcut.repositories import arxiv, libgen_repo
import pandas as pd
from bookcut.search import choose_a_book


def libgen_book_find(title, author, publisher, destination, extension, force, libgenurl):
    ''' searching @ LibGen for a single book '''
    try:
        book = Booksearch(title, author, publisher, type, libgenurl)
        result = book.search()
        extensions = result['extensions']
        tb = result['table_data']
        mirrors = result['mirrors']
        file_details = book.give_result(extensions, tb, mirrors, extension)
        if file_details is not None:
            book.cursor(file_details['url'], destination,
                        file_details['file'], force)
    except TypeError:
        # TODO add logger error
        pass


def book_searching_in_repos(term, repos):
    '''search a book in various Repositories'''
    if repos is None:
        libgen_data = libgen_repo(term)
        return libgen_data
    repos = repos.split(',')
    repos = [i.strip(' ') for i in repos]
    available_repos = settingParser('Repositories', 'available_repos')
    for i in repos:
        if i in available_repos:
            if i == 'arxiv':
                arxiv_data = arxiv(term)
            if i == 'libgen':
                libgen_data = libgen_repo(term)
    df = pd.concat([libgen_data, arxiv_data], ignore_index=True)
    df.index += 1
    print(df[['Author(s)', 'Title', 'Size', 'Extension']])
    choose_a_book(df)


class Booksearch:
    ''' searching libgen original page and returns book details and mirror link'''

    def __init__(self, title, author, publisher, filetype, libgenurl):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.filetype = filetype
        self.mirror = None
        self.libgenurl = libgenurl

    def search(self):
        ''' searching libgen and returns table data, extensions and links'''
        br = mechanize.Browser()
        br.set_handle_robots(False)   # ignore robots
        br.set_handle_refresh(False)  #
        br.addheaders = [('User-agent', 'Firefox')]

        br.open(self.libgenurl)
        br.select_form('libgen')
        input_form = self.title + ' ' + self.author + ' ' + self.publisher
        br.form['req'] = input_form
        ac = br.submit()
        html_from_page = ac
        soup = Soup(html_from_page, 'html.parser')
        links_table = soup.find_all('table')[3]
        table_data = []
        mirrors = []
        extensions = []
        for i in links_table:
            try:
                td = i.find_all('td')
                for tr in td:
                    # scrape mirror links
                    temp = tr.find('a', href=True)
                    mirror_page = temp['href']
                    # add also mirror link
                    if mirror_page.startswith('http') is False:
                        mirror_page = self.libgenurl + temp['href']
                    else:
                        mirror_page = temp['href']
                    mirrors.append(mirror_page)
            except Exception as e:
                    print(e)

            # Parse Details from table_data
            table = soup.find_all('table')[2]
            for i in table:
                try:
                    td = i.find_all('td')
                    row = tr.find_all('tr')
                    row = [tr.text for tr in td]
                    table_data.append(row)
                    extensions.append(row[8])
                    table_details = dict()
                    table_details['extensions'] = extensions
                    table_details['table_data'] = table_data
                    table_details['mirrors'] = mirrors
                    return table_details
                except Exception as e:
                    pass

    def give_result(self, extensions, table_data, mirrors, filetype):
        try:
            if filetype is not None:
                temp = 0
                for i in extensions:
                    if filetype == i:
                        result = dict()
                        result['url'] = mirrors[temp]
                        result['file'] = extensions[temp]
                        print("\nDownloading Link: FOUND")
                        return result
                    temp = temp + 1
            else:
                # return the first result
                result = dict()
                result['url'] = mirrors[0]
                result['file'] = extensions[0]
                print('\nDownloading Link: FOUND')
                return result
        except IndexError:
            print("Downloading Link:NOT FOUND\n")
            print('================================')

    def cursor(self, url, destination_folder,
               extension, forced):
        ''' asking the user to download a chosen book or to abort'''
        title = str(self.title)
        author = str(self.author)
        nameofbook = file_name(url)
        if nameofbook is None:
            nameofbook = title.replace('\n', '') + author.replace('\n', '') + '.' + extension
        if forced is not True:
            ask = confirm(f'Do you want to download:\n {nameofbook}')
            if ask is True:
                downloading(url, title, author, nameofbook, destination_folder,
                            extension)
        else:
            downloading(url, title, author, nameofbook, destination_folder,
                        extension)
