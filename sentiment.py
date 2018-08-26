#!/usr/bin/env python
# -*- coding: utf-8 -*-

from textblob_de import TextBlobDE as TextBlob
import unicodecsv as csv
import sys
import multiprocessing

csv.field_size_limit(sys.maxsize)

def main():
	with open('full_text.csv','rb') as f:

		r = csv.reader(f)
		data = list(r)

	data = data[1:] # no header

	results = []
	results.append(['file_name','abstimmungstag','polarity','subjectivity'])

	# parallel
	pool = multiprocessing.Pool(processes=4)
	results += pool.map(get_sentiment, data)

	#for x in data[0:3]:
	#	results.append(get_sentiment(x))

	with open('sentiment.csv','wb') as aa:
		writer = csv.writer(aa)
		writer.writerows(results)

def get_sentiment(row):

	blob = TextBlob(row[2])
	mood = blob.sentiment

	pol = mood.polarity
	sub = mood.subjectivity

	#print sub
	#print pol

	# polarity is a float within the range [-1.0, 1.0]
	# subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
	
	return [row[0], row[1], pol, sub]


if __name__ == "__main__":
	main()