import pytest
from bookcut.mirror_checker import openLibraryStatus, main as mirror_checker
from bookcut.mirror_checker import requests
from requests import ConnectionError


@pytest.mark.web
def test_mirror_availability():
    available_mirror = mirror_checker()
    assert type(available_mirror) is str, "Not correct type of LibGen Url"
    assert available_mirror.startswith('http'), "Not correct LibGen Url."


@pytest.mark.parametrize("status_code", [200, 301])
def test_openLibraryStatus_output_if_it_can_connect(monkeypatch, capsys, status_code):
    def mock_requests_head(url):
        return type("_", (), {"status_code": status_code})
    monkeypatch.setattr(requests, "head", mock_requests_head)
    assert openLibraryStatus() is None
    captured = capsys.readouterr()
    assert captured.out == "Connected to: http://www.openlibrary.org\n"


def test_openLibraryStatus_output_for_wrong_status_code(monkeypatch, capsys):
    def mock_requests_head(url):
        return type("_", (), {"status_code": 42})
    monkeypatch.setattr(requests, "head", mock_requests_head)
    assert not openLibraryStatus()
    captured = capsys.readouterr()
    assert captured.out == ('Unable to connect to: http://www.openlibrary.org '
                            '\nPlease check your internet connection and try again later.\n')


def test_openLibraryStatus_output_on_connection_error(monkeypatch, capsys):
    def mock_requests_head(url):
        raise ConnectionError
    monkeypatch.setattr(requests, "head", mock_requests_head)
    assert not openLibraryStatus()
    captured = capsys.readouterr()
    assert captured.out == ('\nUnable to connect to: http://www.openlibrary.org '
                            '\nPlease check your internet connection and try again later.\n')

@pytest.mark.web
def test_open_libraryStatus():
    status = openLibraryStatus()
    assert status is not False, "OpenLibrary Status =! 200"
