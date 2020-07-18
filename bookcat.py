import click
import pyfiglet
from db_rules import main as db_main
from os import name, system
from automate import book_search

@click.command()
@click.option('--bookname', '-b' ,prompt = "Book Title", help='The name of the book you wish to download.')
@click.option('--author', '-a',prompt='Author',
              help='The person who wrote the book.' , required=False)
@click.option('--publisher', default = "")
@click.option('--f', default ="", help='A .txt file witch works like a download list')



def main(bookname, author,publisher,f):
    """Simple program that greets NAME for a total of COUNT times."""

    if f:
        Lines = file_list(f)
        print(Lines)
        for a in Lines:
            if a != "":
                print("*** Searching for :", a,'\n')
                nill = ""
                db_main(bookname, author, publisher,f)
                book_search(a,a,nill)
    else:
        book_search(bookname,author,publisher)



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


if __name__ == '__main__':
    clean_screen()
    title= pyfiglet.figlet_format("BookCut")
    print(title,'\n', "**********************************")
    print("Welcome to BookCut!  I'm here to help you \n to read your favourite books! \n")
    main()
