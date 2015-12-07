# config
debug = 0 # 1 = output logs. 0 = do not output logs. 

# import things
import sys, lib, os
lib.debug(debug)

# take in input
category = sys.argv[1]
content = sys.argv[2]

if len(category) == 0:
	print "Category missing. Usage: \npython categorize.py [category] [content]"
	sys.exit()
elif len(content) == 0:
	print "Content missing. Usage: \npython categorize.py [category] [content]"
	sys.exit()

# get the files for the type of categorization they want
categoriesRaw = {}
for file in [f for f in os.listdir("categories/" + category) if (os.path.isfile("categories/" + category + "/" + f) and f[-4:] == ".txt" and f != "stopwords.txt")]:
	categoriesRaw[file[0:-4]] = open("categories/" + category + "/" + file).read()

# build out categories as bag of words
categories = lib.prepareCategories(categoriesRaw)

# apply stop words
f = open("categories/" + category + "/stopwords.txt", "r")
if f:
	stopwords = set(lib.tokenize(f.read()))
	for key in categories:
		categories[key] = [w for w in categories[key] if len(stopwords.intersection([w])) == 0]
	if debug:
		print "\n\nfiltering out stop words: "
		print stopwords

# categorize content passed in 
category = lib.categorize(lib.tokenize(content), categories)

if len(category):
	print category
else:
	print "Not sure"