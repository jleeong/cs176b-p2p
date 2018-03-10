"""python script to deploy docker containers"""
import os
import json
import subprocess
import sys
import random
import argparse
import hashlib
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

parser = argparse.ArgumentParser()
parser.add_argument('-n','--networking',dest='N',type=int,help='generates overlay network with N connections per node')
parser.add_argument('-v',action='store_true',help='verbose output to show file distribution')
parser.add_argument('-m','--mode',default='g', dest='mode',help='[g|d] gnutella or distributed hash table',required=True)
args = vars(parser.parse_args(sys.argv[1:]))

with open("test_data/nodes.json",'r') as nodes:
    raw = ''.join(nodes.readlines())
    initialset = json.loads(raw)
print(initialset)

if args['N'] != None:
    try:
        print("Generating Network")
        # generate the virtual network
        hostfiles = {}
        ir = {}
        total = len(initialset)
        num_connections = args['N']
        if(num_connections > total):
            sys.exit("Too many per node connections.")
        print(str(total)+" nodes found.")
        try:
            # make host files
            for n in initialset:
                hostfiles[n] = open('test_data/networking/'+n+'.hosts','w')
                ir[n] = []

            # populate intermediate representation
            for i in range(num_connections):
                print("Connection: "+str(i))
                workingset = initialset[:]
                networkset = []
                currnode = workingset[0]
                networkset.append(currnode)
                while len(workingset)>1:
                    avail = set(workingset) - set(networkset)
                    #print(currnode, ir[currnode], avail)
                    target = list(avail)[random.randint(1,len(avail))-1]
                    print(" Adding "+currnode+"->"+target+" to network.")
                    ir[currnode].append(target)
                    #ir[target].append(currnode)
                    workingset.remove(target)
                    networkset.append(target)
                    currnode=target
                # last non-connected node
                target = workingset[0]
                print("Adding "+currnode+"->"+target+" to network.")
                ir[currnode].append(target)
                #ir[target].append(currnode)

            print("Final network:")
        finally:
            # write and close host files
            for fname in hostfiles:
                print(fname+":", ir[fname])
                hostfiles[fname].write('\n'.join(set(ir[fname])))
                hostfiles[fname].close()
    except TypeError:
        print("Invalid command line arg. Network not generated.")

# deploy containers
print("Deploying Containers")
docker_image = 'cs176b-p2p'
docker_nw = 'p2p_nw'
if subprocess.check_output(['docker','images','-q',docker_image]).decode('utf-8') == '':
    subprocess.run(['docker','build','-t',docker_image,'.'])
existing_nw = subprocess.check_output(['docker','network','ls']).decode('utf-8')
if  docker_nw not in existing_nw:
    subprocess.run(['docker','network','create',docker_nw])

for c in initialset:
    print(c)
    if c == 'node-0':
        cmd = ['docker','run','--rm','--name',c,'-d','--network',docker_nw,\
            '-v'+os.getcwd()+'/test_data/networking/'+c+'.hosts:/var/cs176/p2p/hosts',\
            '-p8080:8080','--hostname='+c,docker_image]
    else:
        cmd = ['docker','run','--rm','--name',c,'-d','--network',docker_nw,\
            '-v'+os.getcwd()+'/test_data/networking/'+c+'.hosts:/var/cs176/p2p/hosts',\
            '--hostname='+c,docker_image]
    subprocess.run(cmd)

# distribute files
with open('test_data/nodes.json','r') as nodes:
    raw = ''.join(nodes.readlines())
    containers = json.loads(raw)

verbose = args['v']
mode = args['mode']

active_files = []
files = os.listdir('test_data/samples')
files.sort(key=natural_keys)

if(mode == 'g'):
    if verbose: print("distributing randomly as per gnutella routing")
    for targetfile in files:
        index = random.randint(1,len(containers))-1
        c = containers[index]
        if verbose: print(" Copying samplefile "+targetfile+" to "+c)
        subprocess.run(['docker','cp','test_data/samples/'+targetfile ,\
            c+':/var/cs176/p2p/files/'+targetfile])

elif(mode == 'd'):
    if verbose: print("distributing hash(files)modulo #numnodes according to distributed hash tables initialization")
    num_nodes = len(containers) #used for modulo in hash_function
    #hash the
    for targetfile in files:
        m = hashlib.md5(targetfile.encode('utf-8'))
        z = int(m.hexdigest(), 16)
        container_number = z%num_nodes
        if verbose: print(" Copying sample file: "+targetfile)
        active_files.append(targetfile)
        subprocess.run(['docker','cp','test_data/samples/'+targetfile ,\
            containers[container_number]+':/var/cs176/p2p/files/'+targetfile])
