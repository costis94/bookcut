import requests
from requests import ConnectionError
import configparser
import os


CONNECTION_ERROR_MESSAGE = (
    '\nUnable to connect to: {} '
    '\nPlease check your internet connection and try again later.'
)


def settingParser(section, value):
    "Parsing data from Settings.ini"
    config = configparser.ConfigParser()
    module_path = os.path.dirname(os.path.realpath(__file__))
    settings_ini = os.path.join(module_path, 'Settings.ini')
    config.read(settings_ini)
    mirrors = config.get(section, value)
    mirrors = mirrors.split(',')
    return mirrors


def main():
    '''Check which LibGen mirror is available'''

    mirrors = settingParser('LibGen', 'mirrors')
    for url in mirrors:
        try:
            r = requests.head(url)
            if r.status_code == 200 or r.status_code == 301:
                status = True
            if status is True:
                print('Connected to:', url)
                return url
                break
            else:
                print("No mirrors available or no Internet Connection!")
        except:
            pass


def pageStatus(url):
    try:
        request = requests.head(url)
        if request.status_code == 200 or request.status_code == 301:
            print('Connected to:', url)
            return True
    except ConnectionError:
        pass
    print(CONNECTION_ERROR_MESSAGE.format(url))
    return False


if __name__ == '__main__':
    main()
