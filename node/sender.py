class Sender:
	"""Class to encompass the sending functions of a P2P node"""
	def __init__(self):
		print("Sender created")

	def sendFile(destination_info, file_details):
		"""sendFile will construct a TCP connection to the designated
		destination, retrieve the resource defined by file details,
		and perform the data transfer."""
