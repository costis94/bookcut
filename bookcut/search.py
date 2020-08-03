from bookcut.mirror_checker import main as mirror_checker
from bookcut.downloader import pathfinder
from bs4 import BeautifulSoup as Soup
import mechanize
import pandas as pd
import os
import requests
from tqdm import tqdm


def search_downloader(file, href):
    response = requests.get(href, stream=True)
    total_size = int(response.headers.get('content-length'))
    inMb = total_size / 1000000
    inMb = round(inMb, 2)
    filename = file
    print("\nDownloading...\n", "Total file size:", inMb, 'MB')

    path = pathfinder()

    filename = os.path.join(path, filename)
    # progress bar
    buffer_size = 1024
    progress = tqdm(response.iter_content(buffer_size), f"{file}",
                    total=total_size, unit="B", unit_scale=True,
                    unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    print("================================\nFile saved as:", filename)


def link_finder(link):
    page = requests.get(link)
    soup = Soup(page.content, 'html.parser')
    searcher = [a['href'] for a in soup.find_all(href=True) if a.text]
    filename = soup.find('input')['value']

    results = [filename, searcher[0]]
    return results


def search(term):
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

        try:
            tabular = pd.DataFrame(table_data)
            tabular.index += 1
            tabular.columns = headers
            print(tabular)
            choices = []
            temp = len(mirrors) + 1
            for i in range(1, temp):
                choices.append(str(i))
            choices.append('C')
            choices.append('c')
            while True:
                tell_me = str(input('\n\nPlease enter a number from 1 to {number}'
                                    'to download a book or press "C" to abort'
                                    'search: '.format(number=len(extensions))))
                if tell_me in choices:
                    if tell_me == 'C' or tell_me == 'c':
                        print("Aborted!")
                        return None
                    else:
                        c = int(tell_me) - 1
                        print(mirrors[c], "   ", extensions[c])
                        results = [mirrors[c], extensions[c]]
                        return results
        except ValueError:
            print('\nNo results found or bad Internet connection.')
            print('Please,try again.')
            return None
    else:
        print('\nNo results found or bad Internet connection.')
        print('Please,try again.')


if __name__ == '__main__':
    search(input('Term: '))
