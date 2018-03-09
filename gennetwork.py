"""This file will be used to generate the `hosts` files to place into the virtual nodes.
It attempts to create a fully-connected non-directional graph with x amount of connections.
per network node.
    for every node-x in `nodes.yml`:
        create `networking/node-x.hosts`"""
import json
import random
import sys

if len(sys.argv) != 2:
    print("Usage: python3 genhostfiles.py <node_connections>")

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
