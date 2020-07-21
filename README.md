# BookCut

BookCut is a very simple python CLI app, that help the user to download **free ebooks** in epub format.



##REQUIREMENTS

The only requirement is to have installed Python 3.
This is a Python 3 project that will not work with Python2.

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
python setup.py install
```


## Usage

* To download a **single** book:
```bash
python bookcut book -b "White Fang" -a "Jack London"
```
or if you have also python2 installed specify the python version:

```bash
python3 bookcut.py book -b "White Fang" -a "Jack London"
```

* To download a **list** of books:
```bash
python bookcut.py list "FreeEbooksToDownload.txt"
```
or if you have also python2 installed specify the python version:
```bash
python3 bookcut.py list "FreeEbooksToDownload.txt"
```

## TO-DO
* To add organize option, which will organize books in folders according to subjects
* To add option for searching in Sci-Hub
* To add searching option with subject keyword for example "nonfiction"

## Copyrights
Please use the bookcut app to download **only free ebooks** that are legally distributing through *Libgen.*
Bookcut contributors do not have any responsibility for the use of the app.
## Contributing
Pull requests are welcome, this is my first project so be kind.
For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
