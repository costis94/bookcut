import setuptools

setuptools.setup(
    name="BookCat", # Replace with your own username
    version="0.5",
    author="Costis94",
    author_email="gravitymusician@gmail.com",
    description="A small example package",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'tqdm',
        'click',
        'requests',
        'beautifulsoup4',
        'pyfiglet',
        'mechanize']

    )
