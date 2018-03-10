import json
import sys

if not len(sys.argv) >= 2:
    print("Usage: python3 append_nodes.py <num_nodes>")
    sys.exit("ERROR: Unrecognized parameters")

num_nodes = int(sys.argv[1])

with open("test_data/nodes.json",'r') as nodes:
    raw = ''.join(nodes.readlines())
    initialset = json.loads(raw)
initial_length = len(initialset)
for i in range(0, num_nodes): 
    initialset.append("node-%s"% str(i+initial_length))

with open("test_data/nodes.json",'w') as nodes: 
  json.dump(initialset, nodes)
