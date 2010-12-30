import Levenshtein
import sys
from nltk.corpus import wordnet
import RapleafInterest
import string
import time

class RapMatcher:
	def __init__(self, dirname):
		""" 
		Takes the directory name of the interest and log files and creates a list of 
		Rapleaf interest objects, a log to record match info, and a match list
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
		return (word1 == word2)
	
	def __levenshtein_match(self, word1, word2):
		"""
		Tests whether word1 and word2 both have length >= 5
		and are within an edit distance of 1 from each other
		"""
		return ((len(word1) >= 5) and 
		(len(word2) >= 5) and 
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
			for syn2 in synset2:
				syn1 = syn1.upper()
				syn2 = syn2.upper()
				if self.__equality_match(syn1, syn2):
					return True
				elif 1 == self.__levenshtein_match(syn1, syn2):
					return True
		return False
		
	def match(self, query):
		""" Matches a query with a Rapleaf interest """
		self.matches.clear()
		query = query.upper()
		for interest in self.interests:
			for word in interest.get_words():
				word = word.upper()
				if ((self.__equality_match(query, word)) or 
				(self.__levenshtein_match(query, word)) or 
				(self.__wordnet_match(query, word))):
					self.matches.add(interest.get_name())
		return self.matches
