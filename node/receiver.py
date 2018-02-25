from .sender import Sender
import socket
import threading
class Receiver:
	"""Class to encompass the TCP listening functions of the P2P node."""
	def __init__(self):
		"""Constructor for passive TCP receiver on current node. Has
		internal instance of a receiver to perform responses to incoming
		P2P requests"""
		self.sender = Sender()
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
			(cs, sip) = ss.accept()
			t = threading.Thread(target=self.parseRequest,args=(cs,sip))
			t.daemon = True
			t.start()
		print("Listening at :" + str(portnum))

	def parseRequest(self,incoming_socket,source_ip):
		"""parseRequest will parse the received TCP request and return an
		array containing relevant details for further processing"""
		print(tcp_request)

	def respond(self,request_details):
		"""respond will examine the supplied request_details (supplied by
		 parseRequest) and determine the proper action to take. (Send requested
		 file or ignore the request)"""
