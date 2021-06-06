import pytest

from click.testing import CliRunner
from bookcut import __version__
from bookcut.bookcut import entry

def test_entry_with_version_option():
    cli_output = CliRunner().invoke(entry, ["--version"])
    assert cli_output.exit_code == 0
    assert cli_output.output == f"commands, version {__version__}\n"
