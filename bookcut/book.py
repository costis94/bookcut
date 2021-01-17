from bookcut.mirror_checker import main as mirror_checker
import mechanize
from bs4 import BeautifulSoup as Soup
from bookcut.libgen import file_name
from click import confirm
from bookcut.downloader import downloading


def book_find(title, author, publisher, destination, extension, force):
    try:
        book = Booksearch(title, author, publisher, type)
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


class Booksearch:
    ''' searching libgen original page and returns book details and mirror link'''

    def __init__(self, title, author, publisher, filetype):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.filetype = filetype
        self.mirror = None

    def search(self):
        ''' searching libgen and returns table data, extensions and links'''
        url = mirror_checker()
        if url is not None:
            br = mechanize.Browser()
            br.set_handle_robots(False)   # ignore robots
            br.set_handle_refresh(False)  #
            br.addheaders = [('User-agent', 'Firefox')]

            br.open(url)
            br.select_form('libgen')
            input_form = self.title + self.author + self.publisher
            br.form['req'] = input_form
            ac = br.submit()
            html_from_page = ac
            soup = Soup(html_from_page, 'html.parser')
            table = soup.find_all('table')[2]

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
                            #add also mirror link
                            mirror_page = url + temp['href']
                            mirrors.append(mirror_page)
                        j = j + 1
                    row = [tr.text for tr in td]
                    table_data.append(row)
                    extensions.append(row[8])
                except:
                    pass

            table_details = dict()
            table_details['extensions'] = extensions
            table_details['table_data'] = table_data
            table_details['mirrors'] = mirrors
            return table_details
        else:
            print('\nNo results found or bad Internet connection.')
            print('Please,try again.')

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
