import pytest
from bookcut.mirror_checker import openLibraryStatus, main as mirror_checker
from bookcut.mirror_checker import requests
from requests import ConnectionError

TEST_URL = "http://www.sometesturl.com"


@pytest.mark.web
def test_mirror_availability():
    available_mirror = mirror_checker()
    assert type(available_mirror) is str, "Not correct type of LibGen Url"
    assert available_mirror.startswith('http'), "Not correct LibGen Url."


@pytest.mark.parametrize("status_code", [200, 301])
def test_openLibraryStatus_output_if_it_can_connect(monkeypatch, capsys, status_code):
    def mock_requests_head(_):
        return type("_", (), {"status_code": status_code})
    monkeypatch.setattr(requests, "head", mock_requests_head)
    assert openLibraryStatus(TEST_URL) is None
    captured = capsys.readouterr()
    assert captured.out == f"Connected to: {TEST_URL}\n"


def test_openLibraryStatus_output_for_wrong_status_code(monkeypatch, capsys):
    def mock_requests_head(_):
        return type("_", (), {"status_code": 42})
    monkeypatch.setattr(requests, "head", mock_requests_head)
    assert not openLibraryStatus(TEST_URL)
    captured = capsys.readouterr()
    assert captured.out == (f'Unable to connect to: {TEST_URL} '
                            '\nPlease check your internet connection and try again later.\n')


def test_openLibraryStatus_output_on_connection_error(monkeypatch, capsys):
    def mock_requests_head(_):
        raise ConnectionError
    monkeypatch.setattr(requests, "head", mock_requests_head)
    assert not openLibraryStatus(TEST_URL)
    captured = capsys.readouterr()
    assert captured.out == (f'\nUnable to connect to: {TEST_URL} '
                            '\nPlease check your internet connection and try again later.\n')

@pytest.mark.web
def test_open_libraryStatus():
    status = openLibraryStatus()
    assert status is not False, "OpenLibrary Status =! 200"
