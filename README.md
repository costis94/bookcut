
<img src="https://i.imgur.com/ZUX2ehE.png" width="256" height="69">

[![Downloads](https://pepy.tech/badge/bookcut)](https://pepy.tech/project/bookcut) ![pypi](https://img.shields.io/pypi/v/pip.svg)


BookCut is a Python Command Line Interface tool, that help the user to download **free e-books**,
**organise** them in folders by genre, **retrieve** book details by *ISBN* or *title*,
get a list with **all the books from a writer** and save them to .txt file.

*With the help of LibGen, ArXiv and OpenLibrary.*


## REQUIREMENTS

* Python 3
* python3-pip


## Installation

* **Install with pip:**

```bash
pip install bookcut
#or if you have also Python 2
pip3 install bookcut
```


## Usage

### Searching and downloading books:

* Download a **single** book:

```bash
bookcut book -b "White Fang" -a "Jack London"
```

* Download a **list** of books:

```bash
bookcut list "FreeEbooksToDownload.txt"
```

* Organise a **folder** full of e-books to folders according to genre:

```bash
bookcut organise "full/path/to/folder"
```
***
* Search **LibGen**, output the results and download e-book:

```bash
bookcut search -t 'Homer Odyssey'
```

* Search more book repositories with the **--repos** option:
``` bash
bookcut search -t 'Homer Odyssey' --repos 'libgen,arxiv'
```
  **Available book repositories: Libgen, ArXiv**
***

* Get the **details** of a book by **title and author**, or simply **ISBN**.

```bash
bookcut details -b 'Homer Iliad'
```

* Get a list with *all the books* from an **author**,with an option to save to .txt:

```bash
bookcut all-books -author 'Stephen King'
```
***
### Searching and downloading articles:
Now you can use bookcut to search and download **scientific articles**.

 - Search with the Digital Object Identifier:
```
 bookcut article --doi "10.1126/science.196.4287.293"
```
- Search with the exact title:
```  
 bookcut article --title "Ribulose Bisphosphate Carboxylase  A Two-Layered, Square-Shaped Molecule of Symmetry"
```
****
### Configuration
* Also you can change some basic settings of BookCut. For more check:

```bash
bookcut config --help
```

## TO-DO
* Add Tests
* Add documentation
* Add more sources with free e-books
* Fix organiser so it can use all types of files
* Add a logger.

## Copyrights
Please use the bookcut app to download **only free e-books** that are legally distributing through *BookCut repositories.*
Bookcut contributors do not have any responsibility for the use of the tool.
## Contributing
Pull requests are welcome, this is my first project so be kind.
For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
