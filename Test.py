import RapMatcher
import sys

word = sys.argv[1]
matcher = RapMatcher.RapMatcher('/Users/Flume/Documents/rapleaf/matcher/interests.txt')
for match in matcher.match(word):
	print '%s,' %(match),
