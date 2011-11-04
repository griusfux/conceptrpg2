# Networking subpackage

NET_ENCODING = "utf8"

import re

COMMAND_SEP = b"**:"
ARG_SEP = b"$$:"

def parse_request(request):
	"""Takes a network request and returns user, cmd, data"""
	
	req_str = str(request, NET_ENCODING)
	
	regex = re.compile('(.*?)( )(.*?)( )(.*)', re.DOTALL)
	
	# If the regex didn't match, return the whole string as the command
	if regex.match(req_str):
		user = regex.match(req_str).group(1)
		cmd = regex.match(req_str).group(3)
		data = regex.match(req_str).group(5)
	else:
		cmd = req_str
		data = None
		user = None
		
	return user, cmd, data
	
def parse_request_client(request):
	"""Like parse_request without the user"""
	
	req_str = str(request, NET_ENCODING)
	
	regex = re.compile('(.*?)( )(.*)', re.DOTALL)
	
	# If the regex didn't match, return the whole string as the command
	if regex.match(req_str):
		cmd = regex.match(req_str).group(1)
		data = regex.match(req_str).group(3)
	else:
		cmd = req_str
		data = None
		
	return cmd, data