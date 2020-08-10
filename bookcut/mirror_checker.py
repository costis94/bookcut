import requests
import configparser
import logging
import os


def main():
    '''Check which LibGen mirror is available'''

    config = configparser.ConfigParser()
    module_path = os.path.dirname(os.path.realpath(__file__))
    settings_ini = os.path.join(module_path, 'Settings.ini')
    config.read(settings_ini)
    mirrors = config.get("LibGen", "mirrors")
    mirrors = mirrors.split(',')

    for url in mirrors:
        try:
            r = requests.head(url)
            status = r.status_code == 200
            if status is True:
                return url
                break
            else:
                print("No mirrors available or no Internet Connection!")
        except:
            pass


if __name__ == '__main__':
    main()
