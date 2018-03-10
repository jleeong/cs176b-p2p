import json
import sys

if not len(sys.argv) >= 2:
    print("Usage: python3 append_nodes.py <num_nodes>")
    sys.exit("ERROR: Unrecognized parameters")

num_nodes = int(sys.argv[1])

initialset = []
for i in range(0, num_nodes):
    initialset.append("node-%s"% str(i))

with open("test_data/nodes.json",'w') as nodes:
  json.dump(initialset, nodes)
