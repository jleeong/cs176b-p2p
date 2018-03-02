from node import sender
from node import receiver
from node import actor
import threading
import sys

port_number = 8080

def getFile(actor):
	"""getFile will construct relevant information then pass it to
	an actor for execution."""
	filename = input("Enter filename: ")
	results = actor.act('get',[filename,port_number,'0%'])
	if len(results) > 0:
		tuples = [(len(c),i) for i,c in enumerate(results)]
		print("File found at this minimum hop count path:")
		print(results[min(tuples)[1]])
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
	print("Starting node...")
	# read in P2P algorithm type
	if not len(sys.argv)>=2:
		print("Usage python3 runnode.py [g,d,s] [daemon|client]")
		sys.exit("ERROR: Missing P2P Mode")
	mode = sys.argv[1]
	s = sender.Sender(mode)
	r = receiver.Receiver(mode,port_number)
	# construct and run Receiver thread to run as a daemon process,
	# listens passively for incoming TCP requests.
	rthread = threading.Thread(target=r.listen,)
	rthread.daemon = True
	try:
		if(len(sys.argv) < 3):
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
		elif sys.argv[2] == 'daemon':
			print("Running in daemon only mode.")
			rthread.start()
			rthread.join()
		elif sys.argv[2] == 'client':
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
			print("Unrecognized parameters.")
	except KeyboardInterrupt:
		print('')

	# cleanup threads (because rthread.daemon = True, it dies when main
	# process ends.
	print("Cleaning up...")
	print("bye")

if __name__ == "__main__":
	__main__()
