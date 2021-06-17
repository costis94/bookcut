import requests
import json
from requests import ConnectionError
from bookcut.mirror_checker import pageStatus

"""This file is using by ---details command.
   It's main use is to search OpenLibrary for a books' details.
   It's input can be the name of the book or the ISBN.
"""

OPEN_LIBRARY_URL = "http://www.openlibrary.org"


def main(term):
    # searching OpenLibrary and prints the details of a book
    try:
        if term is None:
            term = input(
                "Please enter the book and the author, or the ISBN of the book."
            )
        term = term.replace(" ", "+")
        pageStatus(OPEN_LIBRARY_URL)
        search_url = "http://openlibrary.org/search.json?q=" + term
        jason = requests.get(search_url)
        jason = jason.text
        data = json.loads(jason)
        try:
            data = data["docs"][0]
        except IndexError:
            data = None
            print("Invalid search, please try again.")

        if data is not None:
            author = data["author_name"][0]
            title = data["title_suggest"]
            isbn = data["isbn"]
            first_publish_year = data["first_publish_year"]
            try:
                lang = data["language"]
            except KeyError:
                lang = None

            print("Results for search: ", term, "\n")
            print("Title:", title)
            print("Author(s):", author, "\n")
            print("ISBN(s):", isbn, "\n")
            if lang is not None:
                print(
                    "Language(s): ",
                )
            print("\nFirst published: ", first_publish_year)
    except ConnectionError:
        url = "http://www.openlibrary.com"
        print(
            "Unable to connect to:",
            url,
            "\nPlease check your internet connection and try again later.",
        )
    except json.decoder.JSONDecodeError:
        print("An error occured during the retrieving of data.")
        print("Please try again later.")
