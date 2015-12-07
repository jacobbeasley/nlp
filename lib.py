import nltk
#lemmatizer = nltk.WordNetLemmatizer() # skipping lemmatization because its slow, but might use and cache in production
stemmer = nltk.PorterStemmer()

# stop words are ignored completely
stopwords = set([
	"the", "you", "of", "it", "them", "these", "those", "all", "me", "her", "him", "just", "found", "and", "that", "are", "for", "few", "did"
])

debugging = 0

def debug(isInDebugMode):
	global debugging
	debugging = isInDebugMode

# tokenize a dictionary of categories and their associated sample content
def prepareCategories(categoriesRaw):
	newCategories = {}
	for key in categoriesRaw:
		newCategories[key] = tokenize(categoriesRaw[key])

	if debugging: 
		print "\n\nPrepared categories: "
		print newCategories

	return newCategories

# figure out what category something is in using Naive Bayes Algorithm
def categorize(words, categories):
	# build dictionary of how many words each category has in common
	categoriesWordsCountInCommon = {}
	categoriesWordsInCommon = {}
	for key in categories: 
		categoriesWordsInCommon[key] = set(categories[key]).intersection(words)
		categoriesWordsCountInCommon[key] = len(categoriesWordsInCommon[key])


	# figure out which category matches the most
	maxCategory = max(categoriesWordsCountInCommon, key=lambda x: categoriesWordsCountInCommon[x])
	maxCategoryCount = categoriesWordsCountInCommon[maxCategory]
	totalWithSameMax = len(filter(lambda x: x == maxCategoryCount, categoriesWordsCountInCommon.values()))

	# output debugging stuff
	if debugging: 
		print "\n\nCategorized content"
		print "Content..."
		print words
		print "\n\nwords that matched:"
		print categoriesWordsInCommon
		print "\n\nwords counts that matched (naive bayes):"
		print categoriesWordsCountInCommon

	# return that category
	if maxCategoryCount > 0 and totalWithSameMax == 1:
		return maxCategory
	else: 
		return ""

# return list of words from a given text data
def tokenize(text):
	original = text

	# separate on punctuation
	text = nltk.Text(nltk.wordpunct_tokenize(text))

	# only get words
	text = [w.lower() for w in text if w.isalpha()]

	# get rid of tiny words
	text = [w for w in text if len(w) > 2]

	# skip stop words
	text = [w for w in text if len(stopwords.intersection([w])) == 0]

	# simplify down to just stems
	#text = [lemmatizer.lemmatize(w) for w in text]
	text = [stemmer.stem(w) for w in text]

	# de-duplicate words and order them for readability
	text = sorted(set(text))

	# output debug stuff
	if debugging:
		print "\n\ntokenized text " + original + " into words..."
		print text

	# returns array of words, stemmed
	return text
