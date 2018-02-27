"""This file will be used to move the `hosts` files into their respective
running Docker containers. It also randomly distributes sample files into
nodes' `files/` directory based on percentage file coverage.
Requires >Python 3.5"""
import json
import random
import subprocess
import os
import sys
with open('nodes.json','r') as nodes:
    raw = ''.join(nodes.readlines())
    containers = json.loads(raw)

if len(sys.argv) != 2:
    print("Usage: python3 deploynetwork.py <file-percentage>")
    sys.exit("ERROR: Unrecognized parameters")

file_percent = sys.argv[1]

files = os.listdir('samples')
for c in containers:
    print(c+":")
    # copy over hosts files
    print(" Copying hosts file...")
    subprocess.run(['docker','cp','networking/'+c+'.hosts',c+':/var/cs176/p2p/hosts'])
    # copy over sample files based on file percentage
    for targetfile in numfiles:
        if random.randint(1,100) <= file_percent:
            print(" Copying sample file: "+targetfile)
            subprocess.run(['docker','cp','samples/'+targetfile ,\
                c+':/var/cs176/p2p/files/'+targetfile])

print("Done.")
