"""This file will be used to generate the `hosts` files to place into the virtual nodes.
It attempts to create an acyclic non-directional graph.
    for every node-x in `nodes.yml`:
        create `networking/node-x.hosts`"""
import json
import random

with open("test_data/nodes.json",'r') as nodes:
    raw = ''.join(nodes.readlines())
    workingset = json.loads(raw)
print(workingset)
hostfiles = {}
ir = {}
total = len(workingset)
print(str(total)+" nodes found.")
try:
    # make host files
    for n in workingset:
        hostfiles[n] = open('test_data/networking/'+n+'.hosts','w')
        ir[n] = []

    # populate intermediate representation
    for i,node in enumerate(ir):
        if(total==1):
            numhosts = 1
        else:
            numhosts = random.randint(0,total-1)
        print("Networking "+node+". Adding "+str(numhosts)+" connections...")
        while len(workingset)>0:
            if len(ir[node]) >= numhosts: break
            index = random.randint(0,total-1)
            if not workingset[index] == node:
                print(" Adding "+workingset[index])
                ir[node].append(workingset[index])
                ir[workingset[index]].append(node)
                del(workingset[index])

            total = len(workingset)
    print("Final network:")
finally:
    # write and close host files
    for fname in hostfiles:
        print(fname+":", ir[fname])
        hostfiles[fname].write('\n'.join(ir[fname]))
        hostfiles[fname].close()
