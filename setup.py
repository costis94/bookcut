import setuptools
import sys
import pathlib

if sys.version_info.major < 3:
    print("\nPython 2 is not supported! \nPlease upgrade to Python 3.\n")
    print("Installation of BookCut stopped, please try again with\n"
          'a newer version of Python!')
    sys.exit(1)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="BookCut",
    python_requires='>3.5.2',
    version="1.2.1",
    author="Costis94",
    author_email="gravitymusician@gmail.com",
    description="Command Line Interface app to download ebooks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/costis94/bookcut",
    packages=setuptools.find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    install_requires=[
            'pandas',
            'click>=7.1.2',
            'requests',
            'beautifulsoup4',
            'pyfiglet',
            'tqdm',
            'mechanize'],
    entry_points='''
            [console_scripts]
            bookcut=bookcut.bookcut:entry
            ''',


        )
