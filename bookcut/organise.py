from bookcut.mirror_checker import pageStatus
import os
import shutil
import requests
import json

OPEN_LIBRARY_URL = 'http://www.openlibrary.org'

def main_organiser(directory):
    status = pageStatus(OPEN_LIBRARY_URL)
    if status is not False:
        book_list = get_books(directory)
        # lists only the files in the given directory
        namepath = []
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    namepath.append(entry.name)
        for i in range(0, len(book_list)):
            print("File:", namepath[i])
            try:
                ''' splitting file name to author and book title for using as
                    searching terms to OpenLibrary'''
                a = book_list[i].split('by')
                book = a[1]
                author = a[0]
                a = scraper(book, author)
                print("\n***", book, "  ", author)
                a = a['genre']
                filename = namepath[i]
                cutpaste(directory, a, filename)
            except IndexError:
                try:
                    a = book_list[i].split('-')
                    book = a[1]
                    author = a[0]
                    a = scraper(book, author)
                    print("\n***", book, "  ", author)
                    a = a['genre']
                    filename = namepath[i]
                    cutpaste(directory, a, filename)
                except IndexError:
                    print('Unable to organise this file.\n')
                    pass


def get_books(dir):
    ''' filtering epub, pdf, txt, mobi, djvu files in the given directory
        and return a list with all filenames '''
    epub_list = []
    for file in os.listdir(dir):
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
        try:
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
        except requests.ConnectionError:
            url = 'http://www.openlibrary.com'
            print('Unable to connect to:', url,
                  '\nPlease check your internet connection and try again later.')
            return None


def genre_finder(sub):
    genres = ['Classics', 'Literary', 'Fiction', 'Historical Fiction',
              'Romance', 'Horror', 'Mystery', 'Suspence', 'Fantasy', 'Action',
              'Adventure', 'Science Fiction', 'History', 'Biography',
              'Autobiography', 'Poetry', 'Art', 'Music', 'Humor', 'Religion',
              'Mythology', 'Philosophy', 'Health', 'Science', 'Social Science',
              'Psychology', 'Self-helf', 'Nonfiction']

    if sub in genres:
        return sub
    else:
        return None


def cutpaste(dir, genre, file):
    '''Check if genre folder exists if not it creates one'''
    path = os.path.join(dir, genre)
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
        print("Created folder:", genre)
        filepath = os.path.join(path, file)

    from_path = os.path.join(dir, file)
    dest_path = os.path.join(dir, genre, file)
    shutil.move(from_path, dest_path)
    print('File moved to: ', genre, '\n', '\n', "********************")
