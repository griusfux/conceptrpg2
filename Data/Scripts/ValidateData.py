def ValidateInt(self, tag, text):
	try:
		setattr(self, tag, int(text))
	except (ValueError, TypeError):
		print("Unable to get an int from the %s tag" % tag)
		self.valid = False
		
def ValidateAllowedData(self, tag, text, allowed):
	if text.lower() in allowed:
		setattr(self, tag, text.lower())
	else:
		print("%s is not a valid entry for %s tag. Allowed = %s" % (text, tag, allowed))
		self.valid = False
		
def ValidateBoolean(self, tag, text):
	if text.lower() == "true":
		setattr(self, tag, True)
	elif text.lower() == "false":
		setattr(self, tag, False)
	else:
		print("The %s tag does not contain true or false" % tag)
		self.valid = False
		
def ValidateSplit(self, tag, text, sep):
	split = text.split(sep)
	if len(split) == 2:
		try:
			x, y = [int(i) for i in split]
			setattr(self, tag, text)
		except (ValueError, TypeError):
			print("Invalid ints for %s in %s tag.\n%s values should in the form x%sy where x and y are ints" % (tag, tag, tag, sep))
			self.valid = False
	else:
		print("Unable to parse %s value in %s tag. Make sure the values are seperated by a %s." % (tag, tag, sep))
		self.valid = False
		
def ValidateList(self, tag, text, allowed):
	split = [i.lower() for i in text.split(', ')]
	for item in split:
		if item not in allowed:
			print("%s is not a valid %s" % (item, tag))
			self.valid = False
		setattr(self, tag, split)