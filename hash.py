#!/usr/bin/python

import os, hashlib, datetime, filecmp, sys

# traverse root directory, and list directories as dirs and files as files
# https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk

def usage():
    print("If comparing two filesystem walks against each other, run the program the following way:\n")
    print("python hash.py <filesystemwalk1.txt> <filesystemwalk2.txt>")
    print("Otherwise, run python hash.py -r to run the filesystem walk")
    exit(1)

def dirWalk():
    BUF_SIZE = 65536
    date = datetime.datetime.now()
    with open(str(date) + '_fullWalk.txt', 'w') as g:
        for root, dirs, files in os.walk("/"):
            exclude = ['dev', 'proc', 'run', 'sys', 'tmp', 'var/lib', '/var/run']
            for folder in exclude:
                if folder in dirs:
                    dirs.remove(folder)
            for filename in files:
                fullpath = os.path.join(root, filename)
                sha256 = hashlib.sha256()
                try:
                    with open(fullpath, 'rb') as f:
                        while True:
                            data = f.read()
                            if not data:
                                break
                            sha256.update(data)
                        g.write(fullpath + ' ' + sha256.hexdigest() + ' ' + str(date) + '\n')
                except (IsADirectoryError, FileNotFoundError, PermissionError):
                    pass
                
def compareWalks(file1, file2):
    # reading files
    f1 = open(file1, "r")  
    f2 = open(file1, "r") 
    f3 = open(file1 + '_' + file2 + '_' + 'differences.txt', 'w)
    i = 0
    for line1 in f1:
        i += 1
        for line2 in f2:
            # matching line1 from both files
            if line1 == line2:  
                continue       
            else:
                print("Line ", i, ":")
                # else print that line from both files
                print("\tFile 1:", line1, end='')
                print("\tFile 2:", line2, end='')
                f3.write(line1 + line2 + '\n')
            break
    # closing files
    f1.close()                                       
    f2.close()    
    f3.close()
 
def main():
    x = input("Compare two dirwalks? [y/n]")
    if x == 'y':
        pass
    if x == 'n': 
        dirWalk()
    else:
        print("Not a valid response. ")
        exit(1)

if __name__ == '__main__':
    length = len(sys.argv)
    if length not in [2,3]: 
        usage()
    elif length == 2 and 'r' in sys.argv:
        dirWalk()
    elif length == 3:
        if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
            compareWalks(sys.argv[1], sys.argv[2])
        else:
            print("One of these files is not valid. Exiting.")
            exit(1) 
    else:
        print("Not a valid command for the program. Exiting.")
        exit(1)
