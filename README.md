This is a simple example demonstrating how to categorize content in Python. 

## Setup Instructions

You will need Python 2.7 and NLTK installed (Google it). Then, you can create a new folder in the "categories" for each way you want to categorize content. Inside of that folder, you can then put a ".txt" file with sample content for each category. 

So, directory structure is...
/categories/[type of category]/[category].txt

### Stop Words

If there are words you are finding are causing problems with categorizing things, you can add them to a stopwords.txt file. Words in this file will be ignored and not factored into any calculations that are happening. 

File will be located at...
/categories/[type of category]/stopwords.txt

### Debugging

To debug, just opepn up the top of autosuggest.py or categorize.py and change debug from "0" to "1". Then it will output all kinds of content to help you debug what is going wrong and why something isn't categorizing the way you thought it would. 

### Usage

python categorize.py [category] [content]

For example...

python categorize.py sentiment "I like PeopleNet"

