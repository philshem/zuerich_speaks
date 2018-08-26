#!/usr/bin/env python
# -*- coding: utf-8 -*-

# reads kantonal csv file
# reads full_text.csv, which contains grouped ballot measure
# splits full_text based on keywords
# maps split full_text to individual ballot measure

import unicodecsv as csv
import sys
import pandas as pd

csv.field_size_limit(sys.maxsize)

split_words_bund = ['Abstimmungsfrage lautet']
split_words_zeit = ['Beleuchtender']

year_start = 1980

def main():

	# load csv with meta info
	df = pd.read_csv('data/KANTON_ZUERICH_abstimmungsarchiv_kanton.csv')

	# assign rank to each ballot measure
	df['vorlage_rank'] = df.groupby(['ABSTIMMUNGSTAG', 'ABSTIMMUNGSART_BEZ'])['STAT_VORLAGE_ID'].rank(method='dense').astype(int)
	print df.head()

	# create new field with just file name (no path)
#	df['file_name'] = df


	# read raw text
	with open('full_text.csv','rb') as f:
		r = csv.reader(f)
		data = list(r)[1:] # no header

	output = []

	# split raw text and assign rank	
	for rec in data:
		year = int(rec[1].split('.')[0])

		full_text = rec[2]
		file_name = rec[0]

		full_text_list = []

		if year >= year_start:
			
			if 'Bundesrat.pdf' in rec[0] and any(word in full_text for word in split_words_bund):
				print year, rec[1], rec[0], full_text.count(split_words_bund[0])
				full_text_list = full_text.split(split_words_bund[0])

				ABSTIMMUNGSART_BEZ = u'eidgenössisch'

			elif 'Zeitung.pdf' in rec[0] and any(word in full_text for word in split_words_zeit):
				print year, rec[1], rec[0], full_text.count(split_words_zeit[0])
				full_text_list = full_text.split(split_words_zeit[0])

				ABSTIMMUNGSART_BEZ = u'kantonal'


		# only add if matching
		if len(full_text_list) > 0:

			# skip first element of full text, which is often a header
			for i in xrange(1,len(full_text_list)):
				output.append( [rec[0], rec[1], ABSTIMMUNGSART_BEZ, i, full_text_list[i] ])

	# join split raw text to rank in meta file
	df2 = pd.DataFrame(output, columns=['file_name','ABSTIMMUNGSTAG','ABSTIMMUNGSART_BEZ', 'vorlage_rank','full_text_mapped'])

	# fix data format to make join
	# meta csv has 10.03.1831
	# text csv has 2011.02.13
	df2['ABSTIMMUNGSTAG'] = df2.ABSTIMMUNGSTAG.str[8:10] + '.' + df2.ABSTIMMUNGSTAG.str[5:7] + '.' + df2.ABSTIMMUNGSTAG.str[0:4]

	df_big = pd.merge(df, df2, on=['ABSTIMMUNGSTAG','ABSTIMMUNGSART_BEZ','vorlage_rank'])

	# pandas csv writer was breaking the R code, so we switched to basic csv writer
	#df_big.to_csv('full_text_mapped.csv',encoding='utf-8', index=False, sep='|')

	# convert to normal python array of array (non-pandas)
	to_print = df_big.values.tolist()

	# write output as csv file
	with open('full_text_mapped.csv','wb') as aa:
		writer = csv.writer(aa,delimiter='|',quotechar = '@', quoting=csv.QUOTE_ALL)
		writer.writerows(to_print)

if __name__ == "__main__":
	main()

