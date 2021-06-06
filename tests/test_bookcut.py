import pytest

from click.testing import CliRunner
from bookcut import __version__
from bookcut.bookcut import entry
from bookcut.mirror_checker import openLibraryStatus, main as mirror_checker
from bookcut.book import book_find
from bookcut.book import Booksearch

def test_entry_with_version_option():
    cli_output = CliRunner().invoke(entry, ["--version"])
    assert cli_output.exit_code == 0
    assert cli_output.output == f"commands, version {__version__}\n"


class TestBookCut:
    @pytest.mark.web
    def test_mirror_availability(self):
        global available_mirror
        available_mirror = mirror_checker()
        assert type(available_mirror) is str, "Not correct type of LibGen Url"
        assert available_mirror.startswith('http'), "Not correct LibGen Url."

    @pytest.mark.web
    def test_open_libraryStatus(self):
        status = openLibraryStatus()
        assert status is not False, "OpenLibrary Status =! 200"

    @pytest.mark.web
    def test_single_book_download(self):
        title = "Iliad"
        author = "Homer"
        publisher = " "
        type_format = ' '
        book = Booksearch(title, author, publisher, type_format, available_mirror)
        result = book.search()
        extensions = result['extensions']
        print('extensions: ', extensions)
        tb = result['table_data']
        mirrors = result['mirrors']
        assert mirrors[0].startswith("http"), "Not correct format of Mirror URL."
        assert type(extensions) is list, "Wrong format of extension details."
        file_details = book.give_result(extensions, tb, mirrors, extensions[0])
