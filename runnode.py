from node import sender
from node import receiver
from node import actor
import threading
import sys
import argparse

port_number = 8080

def getFile(actor):
	"""getFile will construct relevant information then pass it to
	an actor for execution."""
	filename = input("Enter filename: ")
	results = actor.act('get',[filename,port_number,'0'])
	if len(results) > 0:
		paths = []
		packet_counts = 0
		for i,c in enumerate(results):
			paths.append((len(c),i))
			packet_counts += int(c[0])
		result = results[min(paths)[1]]
		print("File found at this minimum hop count path:")
		print(result[1:])
		print("Total packets generated", packet_counts*2)
	else:
		print("No results found.")

def helpMsg(actor):
	"""actor parameter is a stub parameter in this function."""
	print("Avaiable options: get|help|exit|list_neighbors|list_files")

def listHosts(actor):
	actor.act('list_neighbors',[])

def listLocalFiles(actor):
	actor.act('list_files',[])

user_options = {
	'get' : getFile,
	'help' : helpMsg,
	'list_neighbors' : listHosts,
	'list_files': listLocalFiles
}
def __main__():
	"""Main program loop. Creates a receiver thread to passively listen
	for incoming TCP connections and starts a main user loop to prompt
	for user action. Uses instances of node.Receiver and node.Sender classes for
	execution. Uses node.Actor abstract class for user input to function call
	mapping"""
	# read in P2P algorithm type
	parser = argparse.ArgumentParser()
	parser.add_argument('-m','--mode',required=True,help='[g|d] gnutella or dht routing mode')
	parser.add_argument('-d','--daemon',action='store_true',help='run in daemon only mode')
	parser.add_argument('-c','--client',action='store_true',help='run in client only mode')
	parser.add_argument('-n','--num_nodes',help='the number of nodes in the p2p network. Define for DHT')
	args = vars(parser.parse_args(sys.argv[1:]))
	mode = args['mode']
	num_nodes = args['num_nodes']
	print("Starting node...")
	s = sender.Sender(mode, num_nodes)
	r = receiver.Receiver(mode,port_number, num_nodes)
	# construct and run Receiver thread to run as a daemon process,
	# listens passively for incoming TCP requests.
	rthread = threading.Thread(target=r.listen,)
	rthread.daemon = True
	try:
		if args['daemon']:
			print("Running in daemon only mode.")
			rthread.start()
			rthread.join()
		elif args['client']:
			print("Running in client only mode.")
			while True:
				# prompt user for input
				uo = input("Prompt:~> ")
				if uo == 'exit':
					break
				elif uo in user_options:
					user_options[uo](s)
				else:
					helpMsg(s)
		else:
			rthread.start()
			# if receiver thread successful, begin REPL loop for main P2P program.
			if(rthread.isAlive()):
				while True:
					# prompt user for input
					uo = input("Prompt:~> ")
					if uo == 'exit':
						break
					elif uo in user_options:
						user_options[uo](s)
					else:
						helpMsg(s)
	except KeyboardInterrupt:
		print('')

	# cleanup threads (because rthread.daemon = True, it dies when main
	# process ends.
	print("Cleaning up...")
	print("bye")

if __name__ == "__main__":
	__main__()
