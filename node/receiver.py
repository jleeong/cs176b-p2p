from .sender import Sender
import socket
import threading
import os
class Receiver:
	"""Class to encompass the TCP listening functions of the P2P node."""
	def __init__(self,m,portnum, num_nodes):
		"""Constructor for passive TCP receiver on current node. Has
		internal instance of a receiver to perform responses to incoming
		P2P requests. m represents the mode to function in and is one of
		[g|d|s] for gnutella, distributed hash tables, and semantic routing
		respectively."""
		self.port = portnum
		self.mode = m
		self.num_nodes = num_nodes
		self.sender = Sender(m, self.num_nodes)


		print("	Receiver created")

	def listen(self):
		"""listen places the Receiver object in an execution loop to listen
		for incoming TCP requests to the designated port. After receiving a
		request, it will determine if the current node has the desired resource
		and respond accordingly"""
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ss.bind(('',self.port))
		ss.listen(10)
		while True:
			(cs, si) = ss.accept()
			t = threading.Thread(target=self.recvRequest,args=(cs,si))
			t.daemon = True
			t.start()
		print("Listening at :" + str(portnum))

	def recvRequest(self,incoming_socket,source_info):
		"""parseRequest will parse the received TCP request and return an
		array containing relevant details for further processing"""
		#print("Received " + source_info[0] + ":"+str(source_info[1]))
		data = incoming_socket.recv(2048).decode("utf-8")
		data = data.split('\n')
		if(len(data)==2):
			self.respond([incoming_socket,data])
		else:
			print("Invalid request: ",data)

	def respond(self,request_details):
		"""respond will examine the supplied request_details (supplied by
		 parseRequest) and determine the proper action to take. (Send requested
		 file or ignore the request)
		 request_details[0] = client facing socket
		 request_details[1] = data
		 """
		if(self.mode == 'g'):
			try:
				cs = request_details[0]
				data = request_details[1]
				filename = data[0].split(' ')[1]
				# metadata[0] = total number of packets generated so far
				# metadata[1] = current node path
				metadata = data[1].split('%')
				# ignore any packets that have our local address in the
				# hop chain to elimitate infinite loops
				if self.sender.local_address not in metadata:
					print(data)
					if filename in os.listdir("files"):
						# file found on local node; append self to hopchain
						# increase packet count; reply to client socket
						metadata.append(self.sender.local_address)
						metadata[0] = str(1)
						response_msg = "HTTP/1.1 200 OK\n"+'%'.join(metadata)
						cs.send(response_msg.encode('utf-8'))
					else:
						# file not on local node; sender class will append to hopchain
						# update packet count; query all neighbors;
						# return the best path of any results and update the number of packets sent
						forward_results = self.sender.sendRequest([filename,self.port,'%'.join(metadata)])
						if len(forward_results)>0:
							paths = []
							packet_count = 0
							for i,c in enumerate(forward_results):
								paths.append((len(c),i))
								packet_count += int(c[0])
							result = forward_results[min(paths)[1]]
							result[0] = str(len(self.sender.known_hosts) + packet_count)
							response_msg = "HTTP/1.1 200 OK\n"+'%'.join(result)
							cs.send(response_msg.encode('utf-8'))
			finally:
				cs.close()
		elif(self.mode == 'd'):
			try:
				cs = request_details[0]
				data = request_details[1]
				filename = data[0].split(' ')[1]
				# metadata[0] = total number of packets generated so far
				# metadata[1] = current node path
				metadata = data[1].split('%')
				# ignore any packets that have our local address in the
				# hop chain to elimitate infinite loops
				if self.sender.local_address not in metadata:
					print(data)
					if filename in os.listdir("files"):
						# file found on local node; append self to hopchain
						# increase packet count; reply to client socket
						print("found file")
						metadata.append(self.sender.local_address)
						metadata[0] = str(1)
						response_msg = "HTTP/1.1 200 OK\n"+'%'.join(metadata)
						cs.send(response_msg.encode('utf-8'))
				else:
					# file not on local node; sender class will append to hopchain
					# update packet count; query all neighbors;
					# return the best path of any results and update the number of packets sent
					print("file not found")
					forward_results = self.sender.sendRequest([filename,self.port,'%'.join(metadata)])
					if len(forward_results)>0:
						paths = []
						packet_count = 0
						for i,c in enumerate(forward_results):
							paths.append((len(c),i))
							packet_count += int(c[0])
						result = forward_results[min(paths)[1]]
						result[0] = str(len(self.sender.known_hosts) + packet_count)
						response_msg = "HTTP/1.1 200 OK\n"+'%'.join(result)
						cs.send(response_msg.encode('utf-8'))
			finally:
				cs.close()
			print("dht")
		elif(self.mode == 's'):
			print("semantic")
		else:
			exception = illegal_mode.IllegalMode(self.mode);
			print(str(exception))
			raise exception
