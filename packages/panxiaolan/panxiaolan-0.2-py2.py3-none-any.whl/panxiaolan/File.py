import os

def file_num(path):
    files = os.listdir(path)
    print("file numbres: %d" (len(files)))
    return len(files)