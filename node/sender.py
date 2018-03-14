from .actor import Actor
from .exceptions import *
import os
import http.client
import socket
import threading
import math
import hashlib

class Sender(Actor):
	"""Class to encompass the sending functions of a P2P node"""
	def __init__(self,args):
		"""Constructor for the Sender class. Needs to scan local filesystem
		to determine what data exists on current node. Uses this information
		to resopnd to P2P requests. m represents the mode to function in and is one of
		[g|d|s] for gnutella, distributed hash tables, and semantic routing
		respectively.
		args[0] = mode
		args[1] = number of nodes in network"""
		self.mode = args[0]
		self.local_address = socket.gethostname()
		self.neighbor_table = []
		if args[1] != None:
			self.number_nodes = int(args[1])
			dummy_string = "node-1"
			#self.my_host_number = socket.gethostname().split('-')
			my_host_number = int(dummy_string.split('-')[1])
			"""initialize neighbor table for distributed hash based on host number"""
			i = 0
			while(len(self.neighbor_table) < math.ceil(math.log2(self.number_nodes))):
				self.neighbor_table.append((my_host_number + 2**i) % self.number_nodes)
				i+=1

		if os.path.isdir("files"):
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
			"list_neighbors":self.showHosts,
			"list_files": self.showlocalFiles
		}
		return mapping[actionString](args)

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
		request_details[1] = destination port;
		request_details[2] = metadata"""
		print("Sending request for "+request_details[0]+"...")
		if(self.mode == 'g'):
			"""gnutella routing broadcasts the request to every known
			neighbor and determines which route to take based on the
			responses."""
			neighbor_connections = []
			metadata = request_details[2].split('%')
			metadata[0] = str(int(metadata[0])+len(self.known_hosts))
			metadata.append(self.local_address)
			try:
				for h in self.known_hosts:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect((h, request_details[1]))
					msg = "GET "+request_details[0]+" HTTP/1.1\n"+'%'.join(metadata)
					s.send(msg.encode('utf-8'))
					neighbor_connections.append(s)
				return self.handle_responses(neighbor_connections)
			finally:
				for conn in neighbor_connections:
					conn.close()
		elif(self.mode == 'd'):
			m = hashlib.md5(request_details[0].encode('utf-8'))
			z = int(m.hexdigest(), 16)
			desired_container_number = z%self.number_nodes
			print("desired_container_number is %d" % desired_container_number)
			distance_from_container = float("inf")
			print("table is ")
			print(self.neighbor_table)
			curr_neighbor = 0
			index = 0
			for neighbor_number in self.neighbor_table:
				distance = abs(neighbor_number - desired_container_number)
				#print("distance is %d" %distance)
				if( distance < distance_from_container ):
					distance_from_container = distance
					curr_neighbor = index
					index+=1
				else:
					break;
			print("final index is %d" %curr_neighbor)
			return []
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
		for i in os.listdir("files"):
			print(i)

	def handle_responses(self,active_connections):
		"""handle_responses takes in a list of HTTPConnections that are created
		when Sender sends a request. It may be one to many HTTPConnections based
		on the mode of operation for sending a request. It creates a thread to
		listen for responses to the request. Returns a list of all responses"""
		responses = []
		threads = []
		# create a thread for each socket created in a request
		# each thread will store result in responses[]
		for sock in active_connections:
			t = threading.Thread(target=self.response_listener,args=(sock,responses))
			t.start()
			threads.append(t)
		# stop execution while waiting for responses
		#print("waiting on responses...")
		for t in threads:
			t.join()
		#print("done.")
		return responses

	def response_listener(self,active_socket,responses):
		"""response_listener is used by handle_responses() to handle each open
		HTTPConnection. Appends a response to responses"""
		resp = active_socket.recv(4096).decode('utf-8')
		if '\n' in resp:
			responses.append(resp.split('\n')[1].split('%'))
		active_socket.close()
