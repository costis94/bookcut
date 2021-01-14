from os import listdir
from os import path
import requests
import json


def get_books(dir):
    ''' filtering epub, pdf, txt, mobi, djvu files in the given directory
        and return a list with all filenames '''
    epub_list = []
    for file in listdir(dir):
        t = file.split('.')
        if file.endswith(".epub"):
            renamed = file.replace('.epub', '')
            renamed = renamed.replace('_', " ")
            epub_list.append(renamed)
        elif file.endswith(".pdf"):
            renamed = file.replace('.pdf', '')
            renamed = renamed.replace('_', " ")
            epub_list.append(renamed)
        elif file.endswith('.txt'):
            renamed = file.replace('.txt', '')
            renamed = renamed.replace('_', " ")
            epub_list.append(renamed)
        elif file.endswith('.mobi'):
            renamed = file.replace('.mobi', '')
            renamed = renamed.replace('_', " ")
            epub_list.append(renamed)
        elif file.endswith('.djvu'):
            renamed = file.replace('.djvu', '')
            renamed = renamed.replace('_', " ")
            epub_list.append(renamed)
    return epub_list


def scraper(book, author):
        ''' parsing the book category from OpenLibrary '''

        book = book.replace(" ", '+')
        author = author.replace(" ", '+')

        search_url = "http://openlibrary.org/search.json?q=" + book + "+" + author
        jason = requests.get(search_url)
        jason = jason.text
        data = json.loads(jason)
        json_formatted_str = json.dumps(data, indent=2)

        book_values = {}
        isbn = None
        author_name = None
        title = None
        subject = None
        try:
            # TODO: to add feature to check all docs

            data = data['docs'][0]
        except IndexError:
            data = None
        if data is not None:
            try:
                isbn = data['isbn'][0]
            except KeyError:
                pass
            try:
                author_name = data['author_name'][0]
            except KeyError:
                pass
            try:
                title = data['title_suggest']
            except KeyError:
                pass
            try:
                subject = data['subject']
            except KeyError:
                pass

        book_values.update([('isbn', isbn), ('author', author_name),('title',title)])
        if subject is not None:
            for a in subject:
                x = genre_finder(a)
                if x is not None:
                    subject = x
                    break
                else:
                    subject = 'Uncategorized'
        else:
            subject = 'Uncategorized'
        book_values.update({'genre': subject})
        return book_values


def genre_finder(sub):
    genres = ['Classics','Literary', 'Fiction', 'Historical Fiction',
    'Romance', 'Horror', 'Mystery', 'Suspence', 'Fantasy', 'Action',
    'Adventure', 'Science Fiction', 'History', 'Biography', 'Autobiography',
     'Poetry', 'Art', 'Music', 'Humor','Religion', 'Mythology', 'Philosophy',
     'Health', 'Science', 'Social Science', 'Psychology', 'Self-helf',
      'Nonfiction']

    if sub in genres:
        return sub
    else:
        return None


def main(dir):
    epub_list = get_books(dir)

if __name__ == '__main__':
    path = path.expanduser('~/Documents/BookCut')
    main(path)
