from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def return_similar(list_one, list_two, threshold=90, limit=5):

	from fuzzywuzzy import fuzz
	from fuzzywuzzy import process
	dicto = {}

	sec = list_two.copy()

	inter = [x for x in list_one if x not in sec]

	for word in inter:

		result = process.extract(word, sec, limit=limit)
		result = [x for x in result if (x[1] >= threshold) and (x[0] != word)] 
		# print(word)  
		# print(result) 

		if len(result) > 0:
				result = result[0]
				dicto[word] = result[0]

	return dicto 


def matcher(pattern, stringo, return_num):
  import re
  searcho = re.search(pattern, stringo).group(return_num)
  print(searcho)