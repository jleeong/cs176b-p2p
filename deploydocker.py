"""python script to deploy docker containers"""
import os
import json
import subprocess
import sys
import random

if len(sys.argv) != 2:
    sys.exit("Usage: python3 deploydocker.py <node_connections>")

# generate the virtual network
with open("test_data/nodes.json",'r') as nodes:
    raw = ''.join(nodes.readlines())
    initialset = json.loads(raw)
print(initialset)
hostfiles = {}
ir = {}
total = len(initialset)
num_connections = int(sys.argv[1])
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

# deploy containers
docker_image = 'cs176b-p2p'
docker_nw = 'p2p_nw'
if subprocess.check_output(['docker','images','-q',docker_image]).decode('utf-8') == '':
    subprocess.run(['docker','build','-t',docker_image,'.'])
existing_nw = subprocess.check_output(['docker','network','ls']).decode('utf-8')
if  docker_nw not in existing_nw:
    subprocess.run(['docker','network','create',docker_nw])

for c in initialset:
    print(c)
    if 'ingress' in c:
        cmd = ['docker','run','--rm','--name',c,'-d','--network',docker_nw,\
            '-v'+os.getcwd()+'/test_data/networking/'+c+'.hosts:/var/cs176/p2p/hosts',\
            '-p8080:8080','--hostname='+c,docker_image]
    else:
        cmd = ['docker','run','--rm','--name',c,'-d','--network',docker_nw,\
            '-v'+os.getcwd()+'/test_data/networking/'+c+'.hosts:/var/cs176/p2p/hosts',\
            '--hostname='+c,docker_image]
    subprocess.run(cmd)
