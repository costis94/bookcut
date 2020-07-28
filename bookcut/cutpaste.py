from bookcut.downloader import pathfinder
import shutil
import os

def main(dir,genre,file):
    '''Check if genre folder exists if not it creates one'''
    try:
        path = os.path.join(dir,genre)
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
            print("Created folder:" , genre)
            filepath = os.path.join(path,file)

        from_path = os.path.join(dir,file)
        dest_path = os.path.join(dir,genre,file)
        shutil.move(from_path, dest_path)
        print('File moved to: ' , genre , '\n', '\n', "********************")
    except:
        # TODO: debug this error
        print("Info: File did not move\n", "********************", '\n')
if __name__ == '__main__':
    path = pathfinder()
    main(path, 'Horror')
