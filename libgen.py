from bs4 import BeautifulSoup as soupa
import requests


def epub_finder(soup):
    table = soup.find('table', attrs = {'class' : 'c'})
    tb = table.find_all('tr')
    data = []
    list1 = []
    epub = "epub"
    for row in tb:
        col = row.find_all('td')
        col = [ele.text.strip() for ele in col]
        xxx = [ele for ele in col if ele]
        #print(xxx)
        #ekkatharisi sfalmatwn
        false_results = ['[1]', '[2]', '[3]', '[4]', '[5]']
        if false_results == xxx:
            pass
        else:
            data.append(xxx)
        #print('\n')
    del data[0]
    count = 0
    for a in data:
        if epub in a:
            break
        else:
            count = count + 1
    spec_detail = str(data[count])
    details = spec_detail.split(',')
    return count

def file_name(url):
    page = requests.get(url)
    soup = soupa(page.content, 'html.parser')

    r = soup.find('input')['value']
    return r
