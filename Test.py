import RapMatcher
import os
import sys

script = sys.argv[0]
word = sys.argv[1]
matcher = RapMatcher.RapMatcher(os.path.realpath(os.path.dirname(sys.argv[0])))
print matcher.match(word)