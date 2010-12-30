import Levenshtein
import sys
from nltk.corpus import wordnet
import RapleafInterest
import string
import time

class RapMatcher:
	
	debug = True				# Turn on to enable logging
	
	def __init__(self, dirname):
		""" 
		Takes the directory name of the interest and log files and creates a list of 
		Rapleaf interest objects, a log to record match info, and a match list
		"""
		filename = dirname + '/interests.txt'
		f = open(filename, 'r')
		self.interests = map(RapleafInterest.RapleafInterest, map(string.rstrip, f.readlines()))
		self.matches = set()
		if RapMatcher.debug:
			filelog = dirname + '/log.txt'
			self.log = open(filelog, 'a')
	
	def __log(self, query, segment, method):
		"""
		Logs matches to the log file
		"""
		if RapMatcher.debug:
			self.log.write('%s matched %s via %s at %s\n' %(query, segment, method, time.asctime()))
		
	def __get_synset(self, word):
		"""
		Returns a list of synonyms for a given word
		"""
		s = []
		for synset in wordnet.synsets(word):
			s += synset.lemma_names
		return s
	
	def __equality_match(self, query):
		"""
		Tests whether or not the query is string equal to any Rapleaf interests
		"""
		for interest in self.interests:
			for word in interest.get_words():
				if query == word.upper():
					current = interest.get_name()
					self.matches.add(current)
					self.__log(query, current, 'Equality')
	
	def __levenshtein_match(self, query):
		"""
		Tests whether or not the query is within a string edit 
		distance of 1 from any Rapleaf interest
		"""
		for interest in self.interests:
			for word in interest.get_words():
				if 1 == Levenshtein.distance(query, word.upper()):
					current = interest.get_name()
					self.matches.add(current)
					self.__log(query, current, 'Edit Distance')
	
	def __wordnet_match(self, query):
		"""
		Tests whether there exists a short WordNet path 
		from the query to any of the Rapleaf interests
		"""
		query_synset = self.__get_synset(query)
		if not query_synset:
			return
		for interest in self.interests:
			for word in interest.get_words():
				word_synset = self.__get_synset(word)
				if not word_synset:
					continue
				for qword in query_synset:
					for wword in word_synset:
						if qword.upper() == wword.upper():
							current = interest.get_name()
							self.matches.add(current)
							self.__log(query, current, 'WordNet')
						if 1 == Levenshtein.distance(qword.upper(), wword.upper()):
							current = interest.get_name()
							self.matches.add(current)
							self.__log(query, current, 'WordNet + Edit Distance')
	
	def match(self, query):
		""" Matches a query with a Rapleaf interest """
		query = query.upper()
		self.__equality_match(query)
		self.__levenshtein_match(query)
		self.__wordnet_match(query)
		return self.matches
