"""This file will be used to randomly distributes sample files into
nodes' `files/` directory based on percentage file coverage.
Requires >Python 3.5"""
import json
import random
import subprocess
import os
import sys
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v',action='store_true',help='verbose output to show file distribution')
parser.add_argument('-m','--mode',default='g', dest='mode',help='[g|d] gnutella or distributed hash table',required=True)
parser.add_argument('percentage',type=int, help='file distribution percentage')

args = vars(parser.parse_args(sys.argv[1:]))

with open('test_data/nodes.json','r') as nodes:
    raw = ''.join(nodes.readlines())
    containers = json.loads(raw)

verbose = args['v']
mode = args['mode']
file_percent = args['percentage']

active_files = []
files = os.listdir('test_data/samples')

if(mode == 'g'):
    print("distributing randomly as per gnutella routing")
    for c in containers:
        if verbose: print(c+":")
        # copy over sample files based on file percentage
        for targetfile in files:
            if random.randint(1,100) <= file_percent:
                if verbose: print(" Copying sample file: "+targetfile)

                active_files.append(targetfile)
                subprocess.run(['docker','cp','test_data/samples/'+targetfile ,\
                    c+':/var/cs176/p2p/files/'+targetfile])
elif(mode == 'd'):
    print("distributing hash(files)modulo #numnodes according to distributed hash tables initialization")
    num_nodes = len(containers) #used for modulo in hash_function
    #hash the
    for targetfile in files:
        #compute docker container in which we will copy the file
        if random.randint(1,100) <= file_percent:
            m = hashlib.md5(targetfile.encode('utf-8'))
            z = int(m.hexdigest(), 16)
            container_number = z%num_nodes
            if verbose: print(containers[container_number]+":")
            # copy over file to container based on hash result
            if verbose: print(" Copying sample file: "+targetfile)
            active_files.append(targetfile)
            subprocess.run(['docker','cp','test_data/samples/'+targetfile ,\
                containers[container_number]+':/var/cs176/p2p/files/'+targetfile])

if verbose: print("active files")
for f in set(active_files):
    print(f)
