import mechanize
from bs4 import BeautifulSoup as Soup
import requests
from bookcut.downloader import file_downloader
from bookcut.libgen import epub_finder, file_name
import pyfiglet


def downloading(link, name, author, file, destination_folder):
    page = requests.get(link)
    resp = page.status_code
    soup = Soup(page.content, 'html.parser')

    searcher = [a['href'] for a in soup.find_all(href=True) if a.text]

    searcher_link = searcher[0]
    file_downloader(searcher_link, name, author, file, destination_folder)


def book_search(name, author, publisher, destination_folder):
    libgen_url = mirror_checker()
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  #
    br.addheaders = [('User-agent', 'Firefox')]



    response = br.open(libgen_url)
    br.select_form('libgen')
    input_form = name + ' ' + author + ' ' + publisher
    br.form['req'] = input_form
    ac = br.submit()
    html_from_page = ac
    soup = Soup(html_from_page, 'html.parser')

    try:
        line_with_epub = epub_finder(soup)
        links_with_text = [a['href'] for a in soup.find_all(title = "libgen", href=True) if a.text]
        Downloading_page = links_with_text[line_with_epub]
        print("\nDownloading Link: FOUND")
        print(Downloading_page)
        nameofbook = file_name(Downloading_page)

        decision = input(' * BookCut found "'+ nameofbook + '" do you want do download? [Y/n] ')
        decision = decision.capitalize()
        while decision != "Y" and decision != "n":
            decision = input(' * BookCut found "'+ nameofbook + '" do you want do download? [Y/n] ')


        if decision == "Y":
            downloading(Downloading_page,name,author,nameofbook,destination_folder)
        elif decision == "N":
            print("\nDownload aborted, try with a different search!")

    except IndexError:
        print("\nDownloading Link:  NOT FOUND")
        pass
    print("================================ \n")
    br.close()


def custom_download():
    title = pyfiglet.figlet_format("BookCut")
    print("**********************************", '\n', title, '\n',"**********************************")

    print("Welcome to BookCut!  I'm here to help you \n to read your favourite books! \n")
    name = input("Name of Book: ")
    author = input("Author: ")
    book_search(name, author, "")

def mirror_checker():
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  #
    br.addheaders = [('User-agent', 'Firefox')]

    mirrors = ['https://libgen.lc/', 'http://libgen.is/', 'https://Libgen.me/',
    'http://gen.lib.rus.ec/', 'https://Libgen.unblockit.id/', 'http://Libgen.unblocked.pet']

    for i in mirrors:
        try:
            response = br.open(i)
            r_url = response.geturl()
            if i == r_url:
                return i    # return working mirror
                break
            else:
                print('No mirrors available or no Internet\n connection!')
        except:
            pass

    br.close()
