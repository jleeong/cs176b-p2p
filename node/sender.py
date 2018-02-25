from .actor import Actor
from .exceptions import no_file_dir
import os
class Sender(Actor):
	"""Class to encompass the sending functions of a P2P node"""
	def __init__(self):
		"""Constructor for the Sender class. Needs to scan local filesystem
		to determine what data exists on current node. Uses this information
		to resopnd to P2P requests"""
		if os.path.isdir("files"):
			self.available_files = os.listdir("files")
			print("	Sender created")
		else:
			exception = no_file_dir.NoFileDir()
			print(exception.__str___())
			raise exception

	def act(self,actionString,args):
		"""act implementation of Actor superclass"""
		print(actionString,args)
		mapping = {
			"get":self.sendRequest,
		}
		mapping[actionString](args)

	def sendFile(self,destination_info, file_details):
		"""sendFile will construct a TCP connection to the designated
		destination, retrieve the resource defined by file details,
		and perform the data transfer."""
		print("Sending "+file_details+" to "+destination_info+"...")

	def sendRequest(self,file_details):
		"""sendRequest accesses the P2P network to query for a desired
		file. Network access and behavior determined by P2P algorithm."""
		print("Sending request for "+file_details+"...")
