class Receiver:
	"""Class to encompass the TCP listening functions of the P2P node."""
	def __init__(self):
		print("Receiver created")
	def listen(portnum):
		"""listen places the Receiver object in an execution loop to listen
		for incoming TCP requests to the designated port. After receiving a
		request, it will determine the current node has the desired resource
		and respond accordingly"""

	def parseRequest(tcp_request):
		"""parseRequest will parse the received TCP request and return an
		array containing relevant details for further processing"""

	def respond(request_details):
		"""respond will examine the supplied request_details (supplied by
		 parseRequest) and determine the proper action to take. (Send requested
		 file or ignore the request)
