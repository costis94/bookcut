import requests

def main():

    mirrors = ['https://libgen.lc/','http://libgen.li/','http://185.39.10.101/', 'http://genesis.lib/']
    for url in mirrors:
        try:
            r = requests.head(url)
            status = r.status_code == 200
            print("Connected to ", url)
            if status == True:
                return url
                break
            else:
                print("No mirrors available or no Internet Connection!")
        except:
            pass
if __name__ == '__main__':
    main()
