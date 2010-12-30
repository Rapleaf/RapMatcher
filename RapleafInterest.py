class RapleafInterest:
	def __init__(self, name):
		""" 
		Takes a string and splits it by "&" to make Rapleaf segments thesaurus friendly
		Replaces each word's spaces with underscores for WordNet formatting
		"""
		self.name = name
		self.words = name.split(' & ')
		for word in self.words:
			word.replace(" ", "_")
	
	def get_words(self):
		""" Returns an array of constituent words """
		return self.words
	
	def get_name(self):
		""" Returns original interest """
		return self.name
