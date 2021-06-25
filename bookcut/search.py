from bookcut.mirror_checker import main as mirror_checker
from bookcut.downloader import filename_refubrished
from bookcut.settings import path_checker
from bs4 import BeautifulSoup as Soup
import mechanize
import pandas as pd
import os
import requests
from tqdm import tqdm

RESULT_ERROR = "\nNo results found or bad Internet connection.\nPlease try again!"


def search_downloader(file, href):
    # search_downloader downloads the book
    response = requests.get(href, stream=True)
    total_size = int(response.headers.get("content-length"))
    inMb = total_size / 1000000
    inMb = round(inMb, 2)
    filename = file
    print("\nDownloading...\n", "Total file size:", inMb, "MB")

    path = path_checker()

    filename = os.path.join(path, filename)
    # progress bar
    buffer_size = 1024
    progress = tqdm(
        response.iter_content(buffer_size),
        f"{file}",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    print("================================\nFile saved as:", filename)


def link_finder(link, mirror_used):
    # link_ finder is searching Libgen for download link and filename
    page = requests.get(link)
    soup = Soup(page.content, "html.parser")
    searcher = [a["href"] for a in soup.find_all(href=True) if a.text]
    try:
        filename = soup.find("input")["value"]
    except TypeError:
        filename = None
    if searcher[0].startswith("http") is False:
        searcher[0] = mirror_used + searcher[0]
    results = [filename, searcher[0]]
    return results


def search(term):
    # This function is used when searching to LibGen with the command
    # bookcut search -t "keyword"

    url = mirror_checker()
    if url is not None:
        br = mechanize.Browser()
        br.set_handle_robots(False)  # ignore robots
        br.set_handle_refresh(False)  #
        br.addheaders = [("User-agent", "Firefox")]

        br.open(url)
        br.select_form("libgen")
        input_form = term
        br.form["req"] = input_form
        ac = br.submit()
        html_from_page = ac
        soup = Soup(html_from_page, "html.parser")
        table = soup.find_all("table")[2]

        table_data = []
        mirrors = []
        extensions = []

        for i in table:
            j = 0
            try:
                td = i.find_all("td")
                for tr in td:
                    # scrape mirror links
                    if j == 9:
                        temp = tr.find("a", href=True)
                        mirrors.append(temp["href"])
                    j = j + 1
                row = [tr.text for tr in td]
                table_data.append(row)
                extensions.append(row[8])

            except:
                pass

        # Clean result page
        for j in table_data:
            j.pop(0)
            del j[8:15]
        headers = [
            "Author(s)",
            "Title",
            "Publisher",
            "Year",
            "Pages",
            "Language",
            "Size",
            "Extension",
        ]

        try:
            tabular = pd.DataFrame(table_data)
            tabular.index += 1
            tabular.columns = headers
            print(tabular)
            choices = []
            temp = len(mirrors) + 1
            for i in range(1, temp):
                choices.append(str(i))
            choices.append("C")
            choices.append("c")
            while True:
                tell_me = str(
                    input(
                        "\n\nPlease enter a number from 1 to {number}"
                        ' to download a book or press "C" to abort'
                        " search: ".format(number=len(extensions))
                    )
                )
                if tell_me in choices:
                    if tell_me == "C" or tell_me == "c":
                        print("Aborted!")
                        return None
                    else:
                        c = int(tell_me) - 1
                        results = [mirrors[c], extensions[c]]
                        return results
        except ValueError:
            print("\nNo results found or bad Internet connection.")
            print("Please,try again.")
            return None
    else:
        print("\nNo results found or bad Internet connection.")
        print("Please,try again.")


def single_search():
    def search(term):
        # This function is used when searching to LibGen with the command
        # bookcut search -t "keyword"

        url = mirror_checker()
        if url is not None:
            br = mechanize.Browser()
            br.set_handle_robots(False)  # ignore robots
            br.set_handle_refresh(False)  #
            br.addheaders = [("User-agent", "Firefox")]

            br.open(url)
            br.select_form("libgen")
            input_form = term
            br.form["req"] = input_form
            ac = br.submit()
            html_from_page = ac
            soup = Soup(html_from_page, "html.parser")
            table = soup.find_all("table")[2]

            table_data = []
            mirrors = []
            extensions = []

            for i in table:
                j = 0
                try:
                    td = i.find_all("td")
                    for tr in td:
                        # scrape mirror links
                        if j == 9:
                            temp = tr.find("a", href=True)
                            mirrors.append(temp["href"])
                        j = j + 1
                    row = [tr.text for tr in td]
                    table_data.append(row)
                    extensions.append(row[8])

                except:
                    pass

            # Clean result page
            for j in table_data:
                j.pop(0)
                del j[8:15]
            headers = [
                "Author(s)",
                "Title",
                "Publisher",
                "Year",
                "Pages",
                "Language",
                "Size",
                "Extension",
            ]

            try:
                tabular = pd.DataFrame(table_data)
                tabular.index += 1
                tabular.columns = headers
                print(tabular)
                choices = []
                temp = len(mirrors) + 1
                for i in range(1, temp):
                    choices.append(str(i))
                choices.append("C")
                choices.append("c")
                while True:
                    tell_me = str(
                        input(
                            "\n\nPlease enter a number from 1 to {number}"
                            ' to download a book or press "C" to abort'
                            " search: ".format(number=len(extensions))
                        )
                    )
                    if tell_me in choices:
                        if tell_me == "C" or tell_me == "c":
                            print("Aborted!")
                            return None
                        else:
                            c = int(tell_me) - 1
                            print(mirrors[c], "   ", extensions[c])
                            results = [mirrors[c], extensions[c]]
                            return results
            except ValueError:
                print("\nNo results found or bad Internet connection.")
                print("Please,try again.")
                return None
        else:
            print("\nNo results found or bad Internet connection.")
            print("Please,try again.")


def choose_a_book(dataframe):
    # asks the user which book to download from the printed DataFrame
    if dataframe.empty is False:
        dataframe.index += 1
        print(dataframe[["Author(s)", "Title", "Size", "Extension"]])

        urls = dataframe["Url"].to_list()
        titles = dataframe["Title"].to_list()
        extensions = dataframe["Extension"].to_list()
        choices = []
        temp = len(urls) + 1
        for i in range(1, temp):
            choices.append(str(i))
        choices.append("C")
        choices.append("c")
        try:
            while True:
                tell_me = str(
                    input(
                        "\n\nPlease enter a number from 1 to {number}"
                        ' to download a book or press "C" to abort'
                        " search: ".format(number=len(urls))
                    )
                )
                if tell_me in choices:
                    if tell_me == "C" or tell_me == "c":
                        print("Aborted!")
                        return None
                    else:
                        c = int(tell_me) - 1
                        filename = titles[c] + "." + extensions[c]
                        filename = filename_refubrished(filename)
                        if urls[c].startswith("https://export.arxiv.org/"):
                            search_downloader(filename, urls[c])
                            return False
                        else:
                            mirror_used = mirror_checker(False)
                            link = mirror_used + urls[c]
                            details = link_finder(link, mirror_used)
                            file_link = details[1]
                            search_downloader(filename, file_link)
                            return False
        except ValueError:
            print(RESULT_ERROR)
            print("Please,try again.")
            return None
    else:
        print(RESULT_ERROR)
