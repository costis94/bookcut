from bs4 import BeautifulSoup as soup
import mechanize
from bookcut.mirror_checker import (
    pageStatus,
    main as mirror_checker,
    CONNECTION_ERROR_MESSAGE,
)
import pandas as pd

ARCHIV_URL = "https://export.arxiv.org/find/grp_cs,grp_econ,grp_eess,grp_math,grp_physics,grp_q-bio,grp_q-fin,grp_stat"
ARCHIV_BASE = "https://export.arxiv.org"


def arxiv(term):
    # Searching Arxiv.org and returns a DataFrame with the founded results.
    status = pageStatus(ARCHIV_URL)
    if status:
        br = mechanize.Browser()
        br.set_handle_robots(False)  # ignore robots
        br.set_handle_refresh(False)  #
        br.addheaders = [("User-agent", "Firefox")]

        br.open(ARCHIV_URL)
        br.select_form(nr=0)
        input_form = term
        br.form["query"] = input_form
        ac = br.submit()
        html_from_page = ac
        html_soup = soup(html_from_page, "html.parser")

        t = html_soup.findAll("div", {"class": "list-title mathjax"})
        titles = []
        for i in t:
            raw = i.text
            raw = raw.replace("Title: ", "")
            raw = raw.replace("\n", "")
            titles.append(raw)
        authors = []
        auth_soup = html_soup.findAll("div", {"class": "list-authors"})
        for i in auth_soup:
            raw = i.text
            raw = raw.replace("Authors:", "")
            raw = raw.replace("\n", "")
            authors.append(raw)
        extensions = []
        urls = []
        ext = html_soup.findAll("span", {"class": "list-identifier"})
        for i in ext:
            a = i.findAll("a")
            link = a[1]["href"]
            extensions.append(str(a[1].text))
            urls.append(ARCHIV_BASE + link)

        arxiv_df = pd.DataFrame(
            {
                "Title": titles,
                "Author(s)": authors,
                "Url": urls,
                "Extension": extensions,
            }
        )

        return arxiv_df
    else:
        print(CONNECTION_ERROR_MESSAGE.format("ArXiv"))
        return None


def libgen_repo(term):
    # Searching LibGen and returns results DataFrame
    try:
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
            html_soup = soup(html_from_page, "html.parser")
            table = html_soup.find_all("table")[2]

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

            tabular = pd.DataFrame(table_data)
            tabular.columns = headers
            tabular["Url"] = mirrors
            return tabular
    except ValueError:
        # create emptyDataframe
        df = pd.DataFrame()
        return df
