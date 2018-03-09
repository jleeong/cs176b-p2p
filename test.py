from node import sender
from datetime import datetime
import sys

port_number = 8080

if not len(sys.argv)==2:
	print("Usage python3 test.py [g,d,s]")
	sys.exit("ERROR: Missing P2P Mode")
mode = sys.argv[1]
s = sender.Sender(mode)
with open('deployedfiles','r') as infiles:
    files = infiles.readlines()
ts = datetime.now().strftime('%H%M%S')
with open('output/test-'+ts+'.csv', 'w') as outfile:
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
