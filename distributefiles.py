"""This file will be used to randomly distributes sample files into
nodes' `files/` directory based on percentage file coverage.
Requires >Python 3.5"""
import json
import random
import subprocess
import os
import sys
with open('test_data/nodes.json','r') as nodes:
    raw = ''.join(nodes.readlines())
    containers = json.loads(raw)

if not len(sys.argv) >= 2:
    print("Usage: python3 distributefiles.py <file-percentage> [-v]")
    sys.exit("ERROR: Unrecognized parameters")

file_percent = sys.argv[1]
verbose = len(sys.argv) == 3 and sys.argv[2]=='-v'
active_files = []

files = os.listdir('test_data/samples')
for c in containers:
    if verbose: print(c+":")
    # copy over sample files based on file percentage
    for targetfile in files:
        if random.randint(1,100) <= int(file_percent):
            if verbose: print(" Copying sample file: "+targetfile)
            active_files.append(targetfile)
            subprocess.run(['docker','cp','test_data/samples/'+targetfile ,\
                c+':/var/cs176/p2p/files/'+targetfile])

for f in set(active_files):
    print(f)
if verbose: print("Done.")
