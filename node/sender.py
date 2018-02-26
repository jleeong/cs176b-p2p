from .actor import Actor
from .exceptions import *
import os
import http.client
import socket
class Sender(Actor):
	"""Class to encompass the sending functions of a P2P node"""
	def __init__(self,m):
		"""Constructor for the Sender class. Needs to scan local filesystem
		to determine what data exists on current node. Uses this information
		to resopnd to P2P requests. m represents the mode to function in and is one of
		[g|d|s] for gnutella, distributed hash tables, and semantic routing
		respectively."""
		self.mode = m
		self.local_adddress = socket.gethostbyname(socket.gethostname())
		if os.path.isdir("files"):
			self.available_files = os.listdir("files")
			print("	Sender created")
		else:
			exception = no_file_dir.NoFileDir()
			print(exception.__str___())
			raise exception
		if os.path.isfile("hosts"):
			# read in known hosts
			with open("hosts") as f:
				self.known_hosts = f.readlines()
			self.known_hosts = [x.strip() for x in self.known_hosts]
		else:
			exception = no_host_file.NoHostFile()
			print(exception.__str___())
			raise exception

	def act(self,actionString,args):
		"""act implementation of Actor superclass"""
		print(actionString,args)
		mapping = {
			"get":self.sendRequest,
			"list":self.showHosts,
			"list_files": self.showlocalFiles
		}
		mapping[actionString](args)

	def sendFile(self,sending_details):
		"""sendFile will construct a TCP connection to the designated
		destination, retrieve the resource defined by file details,
		and perform the data transfer.
		sending_details[0] = filename
		sending_details[1] = destination port"""
		print("Sending "+file_details+" to "+destination_info+"...")

	def sendRequest(self,request_details):
		"""sendRequest accesses the P2P network to query for a desired
		file. Network access and behavior determined by P2P algorithm.
		request_details[0] = filename;
		request_details[1] = destination port."""
		print("Sending request for "+request_details[0]+"...")
		if(self.mode == 'g'):
			"""gnutella routing broadcasts the request to every known
			neighbor and determines which route to take based on the
			responses."""
			neighbor_connections = []
			for h in self.known_hosts:
				req = http.client.HTTPConnection(h+":"+str(request_details[1]))
				req.set_debuglevel(5)
				req.request("GET","/files/"+request_details[0],body=self.local_adddress)
				neighbor_connections.append(req)
			self.handle_responses(neighbor_connections)
		elif(self.mode == 'd'):
			print("dht")
		elif(self.mode == 's'):
			print("semantic")
		else:
			exception = illegal_mode.IllegalMode(self.mode);
			print(str(exception))
			raise exception

	def showHosts(self,args):
		for h in self.known_hosts:
			print(h)

	def showlocalFiles(self,args):
		for i in self.available_files:
			print(i)

	def handle_responses(self,active_connections):
		"""handle_responses takes in a list of HTTPConnections that are created
		when Sender sends a request. It may be one to many HTTPConnections based
		on the mode of operation for sending a request. It creates a thread to
		listen for responses to the request before choosing the best response"""
		responses = []
		threads = []
		# create a thread for each socket created in a request
		# each thread will store result in responses[]
		for sock in active_connections:
			t = threading.Thread(target=self.response_listener,args(sock,responses))
			t.start()
			threads.append(t)
		# stop execution while waiting for responses
		for t in threads:
			t.join()
		# parse through responses and output chosen path
		# find the path with the minimum amount of hops
		tuples = [(c[0],i) for i,c in enumerate(responses)]
		print(responses[min(tuples)[1]])
	def response_listener(self,active_socket,responses):
		"""response_listener is used by handle_responses() to handle each open
		HTTPConnection"""
		resp = active_socket.getresponse()
		responses.append(resp.split('%'))
