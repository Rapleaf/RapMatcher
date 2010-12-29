import Levenshtein
import sys
from nltk.corpus import wordnet
import RapleafSegment
import string
import time

class RapMatcher:
	def __init__(self, fname):
		f = open(fname, 'r')
		self.log = open('/Users/Flume/Documents/rapleaf/matcher/log.txt', 'a')
		self.interests = map(RapleafSegment.RapleafSegment, map(string.rstrip, f.readlines()))
		self.matches = []
	
	def __log(self, query, segment, method, score):
		if not segment in self.matches:
			self.matches.append(segment)
		self.log.write('%s matched %s via %s at %s\n' %(query, segment, method, time.asctime()))
		
	def __synset(self, word):
		s = []
		for synset in wordnet.synsets(word):
			s += synset.lemma_names
		return s
	
	def __member(self, query):
		for interest in self.interests:
			for part in interest.parts():
				if query.upper() == part.upper():
					self.__log(query, interest.segment(), 'Equality', 9)
		return
	
	def __edit(self, query):
		for interest in self.interests:
			for word in interest.parts():
				if 1 == Levenshtein.distance(query.upper(), word.upper()):
					self.__log(query, interest.segment(), 'Edit Distance', 5)
		return
	
	def __net(self, query):
		for interest in self.interests:
			for word in interest.parts():
				query_synset = self.__synset(query)
				if not query_synset:
					continue
				word_synset = self.__synset(word)
				if not word_synset:
					continue
				for q in query_synset:
					for w in word_synset:
						if q.upper() == w.upper():
							self.__log(query, interest.segment(), 'WordNet', 2)
						if 1 == Levenshtein.distance(q.upper(), w.upper()):
							self.__log(query, interest.segment(), 'WordNet + Edit Distance', 1)
		return
	
	def match(self, query):
		""" Matches a query with a Rapleaf interest """
		self.__member(query)
		self.__edit(query)
		self.__net(query)
		return self.matches
