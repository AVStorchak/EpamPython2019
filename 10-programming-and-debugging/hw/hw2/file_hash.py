import hashlib
import sys
from os import listdir
from os.path import isfile, join


def get_hash(file):
    BLOCK_SIZE = 65536
    file_hash = hashlib.sha256()
    with open(file, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()

path = input("Enter the directory path: ")
key = input("Enter the file hash: ")
files = [f for f in listdir(str(path)) if isfile(join(str(path), f))]

for file in files:
    file_path = join(path, file)

    file_hash = get_hash(file_path)
    if file_hash == key:
        sys.stdout.write('hash: {0} at: {1}'.format(file_hash, file_path))


#script to process the output file and make it readable
#import pstats
#from pstats import SortKey
#p = pstats.Stats('D:\GoldenDict\output.txt')
#p.sort_stats(SortKey.CALLS).print_stats()