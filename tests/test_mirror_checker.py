import pytest
from bookcut.mirror_checker import openLibraryStatus, main as mirror_checker


@pytest.mark.web
def test_mirror_availability():
    global available_mirror
    available_mirror = mirror_checker()
    assert type(available_mirror) is str, "Not correct type of LibGen Url"
    assert available_mirror.startswith('http'), "Not correct LibGen Url."


@pytest.mark.web
def test_open_libraryStatus():
    status = openLibraryStatus()
    assert status is not False, "OpenLibrary Status =! 200"
