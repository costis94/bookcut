import click
import pyfiglet
from os import name, system, listdir
from bookcut.automate import book_search
from bookcut.downloader import pathfinder
from bookcut.organise import get_books as get_books
from bookcut.organise import scraper
from bookcut.cutpaste import main as cutpaste
from bookcut.search import search_downloader, link_finder, search
from bookcut.book_details import main as detailing
from bookcut.bibliography import main as allbooks
from bookcut.bibliography import save_to_txt


@click.group(name='commands')
@click.version_option()
def entry():
    clean_screen()
    title = pyfiglet.figlet_format("BookCut")
    click.echo(title)
    click.echo('**********************************')
    print("  Welcome to BookCut!  I'm here to \n"
          'help you to read your favourite books!')
    print(' **********************************')
    """
    for a single book download you can \n
    bookcut.py book --bookname "White Fang" -- author "Jack London"
    \nor  bookcut.py book -b "White Fang" -a "Jack London" \n
*For a more complete help:  bookcut.py [COMMAND] --help\n
*For example: bookcut.py list --help

    """
    pass


@entry.command(name='list', help='Download a list of ebook from a .txt file')
@click.option('--file', '-f',
              help='A .txt file in which books are written in a separate line',
              required=True)
@click.option('--destination', '-d',
              help="The destinations folder of the downloaded books",
              default=pathfinder())
@click.option('--forced',
              help='Forced option, accepts all books for downloading',
              is_flag=True)
def download_from_txt(file, destination, forced):
    if forced:
        force = True
        click.echo(click.style('(!) Forced list downloading', fg='green'))
    else:
        force = False
        Lines = file_list(file)
        click.echo("List imported succesfully!")
        temp = 1
        many = len(Lines)
        for a in Lines:
            if a != "":
                print(f"~[{temp}/{many}] Searching for:", a,)
                temp = temp + 1
            book_search(a, "", "", destination, force)


@entry.command(name='book', help="Download a book in epub format, by inserting"
               '\n the title and the author')
@click.option('--bookname', '-b', help="Title of Book", required=True)
@click.option('--author', '-a', help='The author of the Book', default=" ")
@click.option('--publisher', '-p', default='')
@click.option('--destination', '-d',
              help="The destinations folder of the downloaded books",
              default=pathfinder())
def download_by_name(bookname, author, publisher, destination):
    print("Searching for", bookname, "by", author)
    book_search(bookname, author, publisher, destination, False)


def file_list(filename):
    file1 = open(filename, 'r', encoding='utf-8')
    Lines = file1.readlines()
    for i in Lines:
        if i == '\n':
            Lines.remove(i)
    return Lines


def clean_screen():
    """ Cleans the terminal screen """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


@entry.command(name='organise',
               help='Organise the ebooks in folders according\n to genre')
@click.option('--directory', '-d', help="Directory of source ", required=True,
              default=pathfinder())
@click.option('--output', '-o',
              help="The destination folder of organised books",
              default=pathfinder())
def organiser(directory, output):
    print(" = BookCut is starting to \norganise your books!")
    book_list = get_books(directory)
    namepath = listdir(directory)
    for i in range(0, len(book_list)):
        a = book_list[i].split('-')
        book = a[1]
        author = a[0]
        a = scraper(book, author)
        print("\n***", book, "  ", author)
        a = a['genre']
        filename = namepath[i]
        cutpaste(directory, a, filename)


@entry.command(name='all-books',
               help="Search and return all the books from an author")
@click.option('--author', '-a', required=True, help='Author name')
@click.option('--ratio', '-r', help='Ratio for filtering  book results',
              default='0.7', type=float)
def bibliography(author, ratio):
    print(f'\n ~Searching for all books by {author}~')
    lista = allbooks(author, ratio)
    if lista is not None:
        print('**********************************')
        choice = 'y or n'
        while choice != 'Y' or choice != 'N':
            choice = input('\nDo you wish to save the list? [Y/n]: ')
            choice = choice.capitalize()
            if choice == 'Y':
                save_to_txt(lista, pathfinder(), author)
                break
            elif choice == 'N':
                print('Aborted.')
                break


@entry.command(name='search',
               help='Search LibGen and choose a book to download')
@click.option('--term', '-t', help='Term for searching')
def searching(term):
    c = search(term)
    if c is not None:
        link = c[0]
        details = link_finder(link)
        filename = details[0]
        file_link = details[1]
        search_downloader(filename, file_link)


@entry.command(name='details', help='Search the details of a book')
@click.option('--book', '-b', help='Enter book & author or the ISBN number.',
              required=True, default=None)
def details(book):
    detailing(book)


if __name__ == '__main__':
    entry()
