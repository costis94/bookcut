import setuptools
import sys

if sys.version_info.major < 3:
    print("\nPython 2 is not supported! \nPlease upgrade to Python 3.\n")
    print("Installation of BookCut stopped, please try again with\na newer version of Python!")
    sys.exit(1)


setuptools.setup(
    name="BookCat",
    python_requires='>3.5.2',
    version="1.1",
    author="Costis94",
    author_email="gravitymusician@gmail.com",
    description="Command Line Interface app to download ebooks",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'tqdm',
        'pandas',
        'click',
        'requests',
        'beautifulsoup4',
        'pyfiglet',
        'mechanize'],
    entry_points='''
        [console_scripts]
        bookcut=bookcut.bookcut:entry
        ''',


    )
