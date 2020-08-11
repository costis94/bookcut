import mechanize
from bs4 import BeautifulSoup as Soup
import requests
from bookcut.downloader import file_downloader
from bookcut.libgen import epub_finder, file_name
from bookcut.mirror_checker import main as mirror_checker


def downloading(link, name, author, file, destination_folder):
    '''finds the first available epub and sends the link to file_downloader '''
    page = requests.get(link)
    soup = Soup(page.content, 'html.parser')

    searcher = [a['href'] for a in soup.find_all(href=True) if a.text]

    searcher_link = searcher[0]
    file_downloader(searcher_link, name, author, file, destination_folder)


def book_search(name, author, publisher, destination_folder, force):
    # searching Libgen for a book
    libgen_url = mirror_checker()
    if libgen_url is not None:
        br = mechanize.Browser()
        br.set_handle_robots(False)   # ignore robots
        br.set_handle_refresh(False)  #
        br.addheaders = [('User-agent', 'Firefox')]

        br.open(libgen_url)
        br.select_form('libgen')
        input_form = name + ' ' + author + ' ' + publisher
        br.form['req'] = input_form
        ac = br.submit()
        html_from_page = ac
        soup = Soup(html_from_page, 'html.parser')

        try:
            line_with_epub = epub_finder(soup)
            links_with_text = [a['href'] for a in soup.find_all(title="libgen", href=True) if a.text]
            Downloading_page = links_with_text[line_with_epub]
            print("\nDownloading Link: FOUND")
            print(Downloading_page)
            nameofbook = file_name(Downloading_page)
            if nameofbook is None:
                nameofbook = name.replace('\n', '') + author.replace('\n', '') + '.epub'
            if force is not True:
                decision = input(' * BookCut found "'+nameofbook+'" '
                                 '\nDo you want to download? [Y/n] ')
                decision = decision.capitalize()
                while decision != "Y" and decision != "N":
                    decision = input(' * BookCut found "'+nameofbook+'" '
                                     '\nDo you want to download? [Y/n] ')

                if decision == "Y":
                    downloading(Downloading_page, name, author, nameofbook,
                                destination_folder)
                elif decision == "N":
                    print("\nDownload aborted, try with a different search!")
            else:
                downloading(Downloading_page, name, author,
                            nameofbook, destination_folder)

        except IndexError:
            print("\nDownloading Link:  NOT FOUND")
            pass
        print("================================ \n")
        br.close()
    else:
        print('\nNo mirrors found or bad Internet connection.')
        print('Please,try again.')
