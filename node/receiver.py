from .sender import Sender
import socket
import threading
class Receiver:
	"""Class to encompass the TCP listening functions of the P2P node."""
	def __init__(self,m):
		"""Constructor for passive TCP receiver on current node. Has
		internal instance of a receiver to perform responses to incoming
		P2P requests. m represents the mode to function in and is one of
		[g|d|s] for gnutella, distributed hash tables, and semantic routing
		respectively."""
		self.mode = m
		self.sender = Sender(m)
		print("	Receiver created")

	def listen(self,portnum):
		"""listen places the Receiver object in an execution loop to listen
		for incoming TCP requests to the designated port. After receiving a
		request, it will determine the current node has the desired resource
		and respond accordingly"""
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ss.bind(('',portnum))
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
		print("Received " + source_info[0] + ":"+str(source_info[1]))
		data = incoming_socket.recv(2048).decode("utf-8")
		data = data.split('\n')
		self.respond([incoming_socket,data])

	def respond(self,request_details):
		"""respond will examine the supplied request_details (supplied by
		 parseRequest) and determine the proper action to take. (Send requested
		 file or ignore the request)
		 request_details[0] = client_facing_socket
		 request_details[1] = data
		 """
		if(self.mode == 'g'):
			try:
				cs = request_details[0]
				data = request_details[1]
				print(data)
				filename = data[0].split(' ')[1]
				metadata = data[1].split('%')
				if filename in self.sender.available_files:
					metadata[0] = str(int(metadata[0])+1)
					response_msg = "HTTP/1.1 200 OK\n"+'%'.join(metadata)+self.sender.local_adddress
					cs.send(response_msg.encode('utf-8'))
				else:
					response_msg = "HTTP/1.1 404 NotFound"
					cs.send(response_msg.encode('utf-8'))
			finally:
				cs.close()
		elif(self.mode == 'd'):
			print("dht")
		elif(self.mode == 's'):
			print("semantic")
		else:
			exception = illegal_mode.IllegalMode(self.mode);
			print(str(exception))
			raise exception
