import requests
import json


def main(term):
    if term is None:
        term =input("Please enter the book and the author, or the ISBN of the book.")
    term = term.replace(' ', '+')
    search_url = "http://openlibrary.org/search.json?q=" + term
    jason = requests.get(search_url)
    jason = jason.text
    data = json.loads(jason)
    json_formatted_str = json.dumps(data, indent=2)
    try:
        data = data['docs'][0]
    except IndexError:
        data = None
        print('Invalid search, please try again.')

    if data is not None:
        author = data["author_name"][0]
        title = data['title_suggest']
        isbn = data['isbn']
        first_publish_year = data["first_publish_year"]
        try:
            lang = data['language']
        except KeyError:
            lang = None
        
        print("Results for search: ", term, '\n')
        print("Title:", title)
        print('Author(s):', author, '\n')
        print('ISBN(s):', isbn, '\n')
        if lang is not None:
            print('Language(s): ', )
        print('\nFirst published: ',first_publish_year)

if __name__ == '__main__':
    n = None
    main(n)
