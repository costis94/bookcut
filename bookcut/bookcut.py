import click
import pyfiglet
import shutil
from os import name, system, listdir
from bookcut.automate import book_search, mirror_checker
from bookcut.downloader import pathfinder

from bookcut.organise import get_books as get_books
from bookcut.organise import scraper
from bookcut.cutpaste import main as cutpaste
@click.group(name='commands')
def entry():
    clean_screen()
    title= pyfiglet.figlet_format("BookCut")
    print(title,'\n', "**********************************")
    print("Welcome to BookCut!  I'm here to help you \n to read your favourite books! \n")

    """
    for a single book download you can \n
    bookcut.py book --bookname "White Fang" -- author "Jack London"
    \nor  bookcut.py book -b "White Fang" -a "Jack London" \n
*For a more complete help:  bookcut.py [COMMAND] --help\n
*For example: bookcut.py list --help

    """
    pass

@entry.command(name='list', help='Download a list of ebook from a .txt file')
@click.option('--file','-f', help='A .txt file in which books are written in a separate line' , required = True)
@click.option('--destination','-d', help= "The destinations folder of the downloaded books" , default = pathfinder())
def download_from_txt(file,destination):
        Lines = file_list(file)
        click.echo("List imported!")
        for a in Lines:
            if a != "":
                print("*** Searching for:", a,'\n')
            else:
                pass
            book_search(a,"","",destination)

@entry.command(name = 'book',help = 'Download a book in epub format, by inserting \n the title and the author')
@click.option('--bookname','-b',help="Title of Book", required = True)
@click.option('--author', '-a', help='The author of the Book' , default = " ")
@click.option('--publisher', '-p', default = '')
@click.option('--destination','-d', help= "The destinations folder of the downloaded books" , default = pathfinder())
def download_by_name(bookname,author,publisher,destination):
    print("Searching for", bookname, "by", author)
    book_search(bookname,author,publisher,destination)

def file_list(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    return Lines

def clean_screen():
    """ Cleans the terminal screen """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

@entry.command(name = 'organise',help = 'Organise the ebooks in folders according\n according to genre')
@click.option('--directory','-d',help="Directory of source ", required = True,
default = pathfinder())
@click.option('--output', '-o', help="The destination folder of organised books", default = pathfinder())
def organiser(directory, output):
    print(" = BookCut is starting to \norganise your books!")
    book_list = get_books(directory)
    namepath = listdir(directory)
    for i in range(0,len(book_list)):
        a = book_list[i].split('-')
        book = a[1]
        author = a[0]
        a = scraper(book, author)
        print("\n***",book, "  ", author)
        a = a['genre']
        filename = namepath[i]
        cutpaste(directory, a , filename)





if __name__ == '__main__':
    entry()
