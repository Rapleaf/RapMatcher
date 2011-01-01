class RapleafInterest:
	def __init__(self, name):
		""" 
		Splits by "&" to make Rapleaf segments thesaurus friendly
		Takes phrases and appends constituent words
		Replaces each word's spaces with underscores for WordNet formatting
		"""
		self.name = name
		self.words = name.split(' & ')
		for phrase in self.words:
			parts = phrase.split()
			if len(parts) > 1:
				for word in parts:
					self.words.append(word)
		for i in range(len(self.words)):		
			self.words[i] = self.words[i].replace(' ', '_')
	
	def get_words(self):
		""" Returns an array of constituent words """
		return self.words
	
	def get_name(self):
		""" Returns original interest """
		return self.name
