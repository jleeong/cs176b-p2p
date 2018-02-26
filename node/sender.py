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
			print("gnutella")
			found = False
			for h in self.known_hosts:
				if not found:
					#print(h+str(request_details[1]))
					req = http.client.HTTPConnection(h+":"+str(request_details[1]))
					req.set_debuglevel(5)
					req.request("GET","/files/"+request_details[0],body=self.local_adddress)
					resp = req.getresponse()
					print(resp)
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
