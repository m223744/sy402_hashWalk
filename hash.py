#!/usr/bin/python

import os, hashlib

# traverse root directory, and list directories as dirs and files as files
# https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk

BUF_SIZE = 65536
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
                print('/'.join(path) + ' hash: ' + sha256.hexdigest())
        except IsADirectoryError:
            pass


