import Levenshtein
from nltk.corpus import wordnet
import RapleafInterest
import string

class RapMatcher:
	"""
	This class' constructor takes a list of interests and is called via
	the match function. The match function is passed a tag and returns a dictionary
	which maps a subset of the interests onto scores which indicate how likely it is
	that their respective key matches the tag.
	"""
	equalScore = 15					# Weight attributed to equality
	
	def __init__(self, interests):
		""" 
		Takes a list of string interests and creates a list of 
		RapleafInterest objects in addition to an empty set of matches 
		"""
		self.interests = map(RapleafInterest.RapleafInterest, map(string.rstrip, interests))
		self.scores = {}
		
	def __get_synset(self, word):
		"""
		Returns a list of synonyms for a given word
		"""
		s = []
		for synset in wordnet.synsets(word):
			s += synset.lemma_names
		return s
	
	def __equality_match(self, word1, word2):
		"""
		Returns equalScore if word1 is word2
		"""
		if word1 == word2:
			return RapMatcher.equalScore
		return 0
		
	def __substring_match(self, word1, word2):
		"""
		If one word is a substring of the other, returns the length of that word
		"""
		if (word1 in word2):
			return len(word1)
		elif (word2 in word1):
			return len(word2)
		return 0
							
	def __levenshtein_match(self, word1, word2):
		"""
		If two words are within an edit distance of 1 from each other
		returns the length of the shorter of the two
		"""
		if (1 == Levenshtein.distance(word1, word2)):
			return min(len(word1), len(word2))
	 	return 0
	
	def __wordnet_match(self, word1, word2):
		"""
		Performs a variety of tests on mutual WordNet neighbors and returns
		an overall WordNet score to indicate the closeness of word1 and word2
		"""
		synset1 = self.__get_synset(word1)
		if not synset1:
			return 0
		synset2 = self.__get_synset(word2)
		if not synset2:
			return 0
		wn_score = 0
		for syn1 in synset1:
			syn1 = syn1.upper()
			for syn2 in synset2:
				syn2 = syn2.upper()
				wn_score += (self.__equality_match(syn1, syn2))/2
				wn_score += (self.__substring_match(syn1, syn2))/2
				wn_score += (self.__levenshtein_match(syn1, syn2))/2
		return wn_score
	
	def match(self, query):
		""" 
		Matches a query with a Rapleaf interest 
		"""
		self.scores.clear()
		query = RapleafInterest.RapleafInterest(query.rstrip())
		for query_word in query.get_words():
			query_word = query_word.upper()
			for interest in self.interests:
				score = 0
				for interest_word in interest.get_words():
					interest_word = interest_word.upper()
					score += self.__equality_match(query_word, interest_word)
					score += self.__substring_match(query_word, interest_word)
					score += self.__levenshtein_match(query_word, interest_word)
					score += self.__wordnet_match(query_word, interest_word)
				if score:
					self.scores[interest.get_name()] = score
		return self.scores
