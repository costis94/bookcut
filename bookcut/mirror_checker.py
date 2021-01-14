import requests
import configparser
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


if __name__ == '__main__':
    main()
