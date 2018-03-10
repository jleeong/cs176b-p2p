from node import sender
from datetime import datetime
import sys
import argparse
import os

port_number = 8080

parser = argparse.ArgumentParser()
parser.add_argument('-m','--mode',dest='mode',required=True,help='[g|d] gnutella or distributed hash table routing')
parser.add_argument('label',help='The label to append to the results file. Suggested format: nodes_nodeconn_filedist')
args = vars(parser.parse_args(sys.argv[1:]))
mode = args['mode']

s = sender.Sender(mode)
files = os.listdir('test_data/samples')
with open('output/test-'+args['label']+'.csv', 'w') as outfile:
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
