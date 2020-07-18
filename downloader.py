import requests
from urllib.request import urlopen
from db_rules import updater
from db_rules import file_checker
from tqdm import tqdm
import os

def file_downloader(href,name,author,file):
    #print('Beginning file downloading...')
    response = requests.get(href, stream=True)
    total_size = int(response.headers.get('content-length'))
    inMb = total_size / 1000000
    inMb = round(inMb,2)
    print("\nDownloading...\n","Total file size:" , inMb, 'MB')
###Folder to download books
    filename = file
    if filename != "":
        pass
    else:
        filename = name + ' - ' + author + ".epub"
    path = os.path.expanduser('~/Documents/BookCat')
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)

    filename = os.path.join(path,filename)

    with open(filename,'wb') as f:
        ''' For progress bar '''
        with tqdm(total=total_size, unit='iB',
               unit_scale=True) as pbar:
            for ch in response.iter_content(chunk_size=1024):
              if ch:
                  f.write(ch)
                  pbar.update(len(ch))

    print("================================\nFile saved as:",filename)
