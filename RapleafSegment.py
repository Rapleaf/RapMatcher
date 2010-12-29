class RapleafSegment:
	def __init__(self, name):
		self.name = name
		self.words = name.split(' & ')
		for word in self.words:
			word.replace(" ", "_")
	
	def parts(self):
		return self.words
	
	def segment(self):
		return self.name
