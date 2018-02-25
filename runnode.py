from node import sender
from node import receiver
from node import actor
import threading

def getFile(actor):
	"""getFile will construct relevant information then pass it to
	an actor for execution."""
	filename = input("Enter filename: ")
	actor.act('get',filename)

def helpMsg(actor):
	"""actor parameter is a stub parameter in this function."""
	print("Avaiable options: get|help|exit")

user_options = {
	'get' : getFile,
	'help' : helpMsg
}
def __main__():
	"""Main program loop. Creates a receiver thread to passively listen
	for incoming TCP connections and starts a main user loop to prompt
	for user action. Uses instances of node.Receiver and node.Sender classes for
	execution. Uses node.Actor abstract class for user input to function call
	mapping"""
	print("Starting node...")
	s = sender.Sender()
	r = receiver.Receiver()
	# construct and run Receiver thread to run as a daemon process,
	# listens passively for incoming TCP requests.
	rthread = threading.Thread(target=r.listen,args=(80,),)
	rthread.daemon = True
	rthread.start()
	# begin REPL loop for main P2P program.
	try:
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
