from bookcut.book import book_find
from bookcut.mirror_checker import main as mirror_checker

def file_list(filename):
    '''checks if the input file is a .txt file and adds each separate line
       as a book to the list 'Lines'.
       After return this list to download_from_txt
    '''

    if filename.endswith('.txt'):
        try:
            file1 = open(filename, 'r', encoding='utf-8')
            Lines = file1.readlines()
            for i in Lines:
                if i == '\n':
                    Lines.remove(i)
            return Lines
        except FileNotFoundError:
            print('Error:No such file or directory:', filename)
    else:
        print("\nError:Not correct file type. Please insert a '.txt' file")


def booklist_main(file,destination,forced,extension):
    '''executes with the command --list'''
    Lines = file_list(file)
    if Lines is not None:
        print("List imported succesfully!")
        url = mirror_checker()
        if url is not None:
            temp = 1
            many = len(Lines)
            for a in Lines:
                if a != "":
                    print(f"~[{temp}/{many}] Searching for:", a,)
                    temp = temp + 1
                    book_find(a, '', '', destination, extension, forced, url)
