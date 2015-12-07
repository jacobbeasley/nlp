# config
debug = 0 # 1 = output logs. 0 = do not output logs. 

# import things
import sys, lib, os, nltk
lib.debug(debug)

# take in input
category = sys.argv[1]
content = sys.argv[2].strip().lower()

if len(category) == 0:
	print "Category missing. Usage: \npython categorize.py [category] [content]"
	sys.exit()
elif len(content) == 0:
	print "Content to autosuggest for missing. Usage: \npython categorize.py [category] [content]"
	sys.exit()

# get sample data
allContent = ""
for file in [f for f in os.listdir("categories/" + category) if (os.path.isfile("categories/" + category + "/" + f) and f[-4:] == ".txt" and f != "stopwords.txt")]:
	allContent += open("categories/" + category + "/" + file).read()

# break into sentences and detect colocations
text = allContent
text = nltk.word_tokenize(text)
text = [w.lower() for w in text]

# build collocation index
collocations = {}
endOfSentence = ['.', ',', '!', '?']

for i in range(0, len(text) - 2):
	thisWord = text[i]
	nextWord = text[i+1]

	if len(set(endOfSentence).intersection([nextWord])) == 0:
		if (not thisWord in collocations):
			collocations[thisWord] = {}

		if (not nextWord in collocations[thisWord]):
			collocations[thisWord][nextWord] = 1
		else:
			collocations[thisWord][nextWord] += 1

# see what next word might be 
words = nltk.word_tokenize(content)
lastWord = words[-1]

if lastWord in collocations.keys():
	# we found the word, so suggest next word!
	matchesList = []
	for match in collocations[lastWord]:
		matchesList.append({
			"nextWord": match,
			"count": collocations[lastWord][match]
		})
	matchesList = sorted(matchesList, key = lambda x: x["count"], reverse = True)

	for match in matchesList:
		print match["nextWord"] + "\t" + str(match["count"]) + " times"
else: 
	# we did not find the word, but is it a partial-match of any?
	partialMatchKeys = [k for k in collocations.keys() if k[0:len(lastWord)] == lastWord]

	if (len(partialMatchKeys)):
		# build list of matches and how often they ewre used
		partialMatches = []
		for match in partialMatchKeys:
			count = 0
			for key in collocations[match]:
				count += collocations[match][key]

			partialMatches.append({
				"nextWord": match,
				"count": count
				})

		# sort it and output results
		partialMatches = sorted(partialMatches, key = lambda x: x["count"], reverse = True)
		for match in partialMatches:
			print match["nextWord"] + "\t" + str(match["count"]) + " times"
	else:
		print "no matches found"