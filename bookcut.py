import click
import pyfiglet
from os import name, system
from bookcut.automate import book_search, mirror_checker
from bookcut.downloader import pathfinder

'''
@click.command()
@click.option('--bookname', '-b' ,prompt = "Book Title", required= True, help='The name of the book you wish to download.')
@click.option('--author', '-a',prompt='Author',
              help='The person who wrote the book.' , required=False)
@click.option('--publisher', '-p', default = " ")
@click.option('--file', '-f',default ="", help='A .txt file witch works like a download list')
'''

@click.group(name='commands')
def entry():
    """Commands"""
    pass

def main(bookname, author,publisher,file):
    """Simple program that greets NAME for a total of COUNT times."""



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


if __name__ == '__main__':
    clean_screen()
    title= pyfiglet.figlet_format("BookCut")
    print(title,'\n', "**********************************")
    print("Welcome to BookCut!  I'm here to help you \n to read your favourite books! \n")
    entry()
