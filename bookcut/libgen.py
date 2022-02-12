from bs4 import BeautifulSoup as soupa
import requests
from bookcut.downloader import file_downloader
from click import confirm
from bookcut.search import RESULT_ERROR


def epub_finder(soup):
    table = soup.find("table", attrs={"class": "c"})
    tb = table.find_all("tr")
    data = []
    epub = "epub"
    for row in tb:
        col = row.find_all("td")
        col = [ele.text.strip() for ele in col]
        xxx = [ele for ele in col if ele]

        false_results = ["[1]", "[2]", "[3]", "[4]", "[5]"]
        if false_results == xxx:
            pass
        else:
            data.append(xxx)
    del data[0]
    count = 0
    for a in data:
        if epub in a:
            break
        else:
            count = count + 1
    return count


def file_name(url):
    print("URL: ", url)
    page = requests.get(url)
    try:
        soup = soupa(page.content, "html.parser")
        r = soup.find("input")["value"]
        r.replace("\n", "")
        return r
    except TypeError:
        return None


def md5_search(md5, url, destination):
    try:
        # function that using by book command and searching for a specific book in LibGen with a given md5 value
        mirror_url = url + "/ads.php?md5=" + md5
        req = requests.get(mirror_url)
        soup = soupa(req.content, "html.parser")
        html = soup.find("input", attrs={"id": "textarea-example"})
        filename = html["value"]
        url_soup = soup.findAll("table", attrs={"id": "main"})

        urls = []
        for j in url_soup:
            a = j.findAll("a", href=True)
            for i in a:
                urls.append(i["href"])
        download_url = url + urls[0]
        question = confirm(f"Do you want to download:\n{filename}")
        if question is True:
            file_downloader(download_url, "", "", filename, destination, "")
        else:
            print("Aborted!")
    except TypeError:
        print(RESULT_ERROR)
