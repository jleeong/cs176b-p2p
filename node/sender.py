class Sender(Actor):
	"""Class to encompass the sending functions of a P2P node"""
	def __init__(self):
		print("	Sender created")
	def act(actionString,params):
		"""act implementation of Actor superclass"""
		
	def sendFile(destination_info, file_details):
		"""sendFile will construct a TCP connection to the designated
		destination, retrieve the resource defined by file details,
		and perform the data transfer."""

	def sendRequest(file_details):
		"""sendRequest accesses the P2P network to query for a desired
		file. Network access and behavior determined by P2P algorithm."""
