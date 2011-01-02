import Levenshtein
from nltk.corpus import wordnet
import RapleafInterest
import string

class RapMatcher:
	minSubstring = 5			# Minimum length of a substring in substring match
	minLevenshtein = 5		# Minimum length of each pair member in Levenshtein match
	
	def __init__(self, dirname):
		""" 
		Takes the directory name of the interest file and creates 
		a list of Rapleaf interest objects and match set
		"""
		fname = dirname + '/interests.txt'
		f = open(fname, 'r')
		self.interests = map(RapleafInterest.RapleafInterest, map(string.rstrip, f.readlines()))
		self.matches = set()
		
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
		Tests whether or not word1 is equal to word2
		"""
		return word1 == word2
		
	def __substring_match(self, word1, word2):
		"""
		Tests whether either word has length greater than 3
		and is a substring of the other word
		"""
		return (((len(word1) >= RapMatcher.minSubstring) and (word1 in word2)) or
		((len(word2) > RapMatcher.minSubstring) and (word2 in word1)))
		
	def __levenshtein_match(self, word1, word2):
		"""
		Tests whether word1 and word2 both have length >= 5
		and are within an edit distance of 1 from each other
		"""
		return ((len(word1) >= RapMatcher.minLevenshtein) and 
		(len(word2) >= RapMatcher.minLevenshtein) and 
		(1 == Levenshtein.distance(word1, word2)))
	
	def __wordnet_match(self, word1, word2):
		"""
		Tests whether there exists a short WordNet path 
		from the word1 to word2, extends via Levenshtein
		"""
		synset1 = self.__get_synset(word1)
		if not synset1:
			return False
		synset2 = self.__get_synset(word2)
		if not synset2:
			return False
		for syn1 in synset1:
			syn1 = syn1.upper()
			for syn2 in synset2:
				syn2 = syn2.upper()
				if self.__equality_match(syn1, syn2):
					return True
				if self.__levenshtein_match(syn1, syn2):
					return True
		return False
	
	def match(self, query):
		""" Matches a query with a Rapleaf interest """
		self.matches.clear()
		query = RapleafInterest.RapleafInterest(query.rstrip())
		for query_word in query.get_words():
			query_word = query_word.upper()
			for interest in self.interests:
				for interest_word in interest.get_words():
					interest_word = interest_word.upper()
					if ((self.__equality_match(query_word, interest_word)) or
					(self.__substring_match(query_word, interest_word)) or
					(self.__levenshtein_match(query_word, interest_word)) or 
					(self.__wordnet_match(query_word, interest_word))):
						self.matches.add(interest.get_name())
		return self.matches
