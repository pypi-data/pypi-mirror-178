import os

def file_num(path):
    files = os.listdir(path)
    print("file numbres: {}".format(len(files)))
    return len(files)