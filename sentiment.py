#!/usr/bin/env python
# -*- coding: utf-8 -*-

# reads full_text.csv
# assigns sentimatent (polarity, subjectivity) to each text
# writes to sentiment.csv

from textblob_de import TextBlobDE as TextBlob
import readability
import unicodecsv as csv
import sys
import multiprocessing

csv.field_size_limit(sys.maxsize)

def main():
	with open('full_text_mapped.csv','rb') as f:
		r = csv.reader(f,delimiter='|', quotechar='@')
		data = list(r)

	results = []
	results.append(data[0] + ['polarity','subjectivity','readability'])

	data = data[1:] # no header

	# parallel
	pool = multiprocessing.Pool(processes=4)
	results += pool.map(get_sentiment, data)

	#for x in data[0:3]:
	#	results.append(get_sentiment(x))

	with open('full_text_mapped_sentiment.csv','wb') as aa:
		writer = csv.writer(aa, delimiter='|',quotechar = '@', quoting=csv.QUOTE_ALL)
		writer.writerows(results)

def get_sentiment(row):

	# last column of each row is the text

	# polarity and subjectivity
	blob = TextBlob(row[-1])
	mood = blob.sentiment

	pol_score = mood.polarity
	sub_score = mood.subjectivity

	# polarity is a float within the range [-1.0, 1.0]
	# subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

	# readability
	rb = readability.getmeasures(row[-1], lang='de')
	rb_score = rb['readability grades']['FleschReadingEase']

	return [row, pol_score, sub_score, rb_score]


if __name__ == "__main__":
	main()