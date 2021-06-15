import pytest
from bookcut.mirror_checker import main as mirror_checker
from bookcut.book import Booksearch


@pytest.mark.web
def test_single_book_download():
    title = "Iliad"
    author = "Homer"
    publisher = " "
    type_format = " "
    book = Booksearch(title, author, publisher, type_format, mirror_checker())
    result = book.search()
    extensions = result["extensions"]
    print("extensions: ", extensions)
    tb = result["table_data"]
    mirrors = result["mirrors"]
    assert mirrors[0].startswith("http"), "Not correct format of Mirror URL."
    assert type(extensions) is list, "Wrong format of extension details."
    file_details = book.give_result(extensions, tb, mirrors, extensions[0])
