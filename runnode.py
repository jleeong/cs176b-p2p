from node import sender
from node import receiver
import threading

def __main__():
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
			ui = input("Prompt:")
			if ui == 'exit':
				break
			print(test)
	except KeyboardInterrupt:
		print('')
	print("Cleaning up...")
	print("	Closing Receiver...",end='')
	rthread.join()
	print("done")
	print("bye")

if __name__ == "__main__":
	__main__()
