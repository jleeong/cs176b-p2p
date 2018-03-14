from node import sender
from datetime import datetime
import sys
import argparse
import os
import re

port_number = 8080
#helper functions
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]
def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b

parser = argparse.ArgumentParser()
parser.add_argument('-m','--mode',dest='mode',required=True,help='[g|d] gnutella or distributed hash table routing')
parser.add_argument('num_nodes',help='total number of nodes in the network.')
parser.add_argument('num_files',help='total number of files distributed through the network.')
args = vars(parser.parse_args(sys.argv[1:]))
mode = args['mode']
num_nodes = args['num_nodes']
s = sender.Sender([mode,num_nodes])
files = os.listdir('test_data/samples')
files.sort(key=natural_keys)

# record the network in a .dot file
with open('output/network-'+args['num_nodes']+'_'+args['num_files']+'.dot', 'w') as outfile:
    print("Recording network...")
    hostfiles = os.listdir('test_data/networking')
    #containers = [ i.split('.')[0] for i in hostfiles if not i == '.gitkeep']
    edges = []
    ir = {} # dictionary mapping node to a list of neighbors
    fd = {} # dictioary mapping node to the number of files it contains
    saturated = 0 # the file count of the most saturated node
    for fname in hostfiles:
        nodename = fname.split('.')[0]
        inf = open('test_data/networking/'+fname,'r')
        ir[nodename] = [ i.rstrip() for i in inf.readlines() ]
        inf.close()
        nodefiles = os.listdir('test_data/container_volumes/'+nodename)
        fd[nodename] = len(nodefiles)
        if(fd[nodename] > saturated): saturated = len(nodefiles)
    print(ir)
    outfile.write('graph '+args['num_nodes']+' {\n')
    for k in ir:
        for i in ir[k]:
            e = (k.split('-')[1],i.split('-')[1])
            if (e[1],e[0]) not in edges:
                edges.append(e)

    for edge in edges:
        line = edge[0]+' -- '+edge[1]+'\n'
        outfile.write(line)
    for n in fd:
        line = n.split('-')[1] + ' [shape=circle,style=filled,fillcolor="#%02x%02x%02x"]\n' % rgb(0,saturated,fd[n])
        outfile.write(line)
    outfile.write('}')

# Retrieve Files from docker network
with open('output/test-'+args['num_nodes']+'_'+args['num_files']+'.csv', 'w') as outfile:
    print("Retrieving files...")
    outfile.write('Filename,Packet Count,Minimum Hop Length,Hop Chain\n')
    for f in files:
        results = s.sendRequest([f.rstrip(),port_number,'0'])
        paths = []
        packet_counts = 0
        for i,c in enumerate(results):
            paths.append((len(c),i))
            packet_counts += int(c[0])
        result = results[min(paths)[1]]
        print("     Minimum hop path:       ",result[1:])
        print("     Total packets generated:    ", packet_counts*2)
        outfile.write(f.rstrip()+','+str(packet_counts*2)+','+str(len(result[1:]))+','+';'.join(result[1:])+'\n')
