def pytest_addoption(parser):
    parser.addoption('--web', action='store_true', dest="web",
                 default=False, help="enable tests requiring an internet connection")

def pytest_configure(config):
    if not config.option.web:
        setattr(config.option, 'markexpr', 'not web')
