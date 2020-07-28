
## BookCut

BookCut is a very simple python CLI app, that help the user to download **free e-books** in e-pub format.



## REQUIREMENTS

* Python 3
* python3-pip


## Installation

*    **Download** or **clone** the project:

```bash
git clone https://github.com/costis94/bookcut
```

* Ensure that an up-to-date version of **setuptools** is installed:
```bash
python -m pip install --upgrade setuptools
```

* cd into the root directory where setup.py is located

* Install project:

```bash
sudo python setup.py install
```


## Usage

* To download a **single** book:
```bash
bookcut book -b "White Fang" -a "Jack London"
```

* To download a **list** of books:
```bash
bookcut list "FreeEbooksToDownload.txt"
```

* To organize a **folder** full of e-books to folders according to genre:
```bash
bookcut organise "full/path/to/folder"
```

## TO-DO
* Add Interactive mode with TUI
* To add option for searching in Sci-Hub
* To add searching option with subject keyword for example "nonfiction"
* To add a simple logger.

## Copyrights
Please use the bookcut app to download **only free e-books** that are legally distributing through *Libgen.*
Bookcut contributors do not have any responsibility for the use of the app.
## Contributing
Pull requests are welcome, this is my first project so be kind.
For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
