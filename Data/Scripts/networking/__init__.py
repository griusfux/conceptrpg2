# Copyright (C) 2011-2012 Mitchell Stokes and Daniel Stokes

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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