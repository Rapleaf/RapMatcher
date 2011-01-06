import RapMatcher
import os
import sys

script = sys.argv[0]
word = sys.argv[1]
fname = os.path.realpath(os.path.dirname(sys.argv[0])) + '/interests.txt'
interests = open(fname, 'r').readlines()
matcher = RapMatcher.RapMatcher(interests)
print matcher.match(word)
