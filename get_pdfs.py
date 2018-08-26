#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import requests
import os
import multiprocessing

def main():
	# read csv
	df = pd.read_csv('data/KANTON_ZUERICH_abstimmungsarchiv_kanton.csv')

	df['dt'] = pd.to_datetime(df.ABSTIMMUNGSTAG)
	#print df.URL_VOLKSABSTIMMUNG.head()
	print df.head()
#	df.assign(pdf_text = df.URL_VOLKSABSTIMMUNG.apply(pdf_text_extractor))
	
	print df.columns

	# get list of urls
	urllist = df[['URL_VOLKSABSTIMMUNG','URL_VOLKSABSTIMMUNG','URL_AMTSBLATT']].values.tolist()

	# flatten list of lists
	urllist = [item for sublist in urllist for item in sublist]

	# remove duplicates
	urllist = list(set(urllist))

	# remove nan
	urllist =  [x for x in urllist if str(x) != 'nan']

	# download
	#for url in urllist:
	#	if url not in ['nan']:
	#		print url
		#	pdf_downloader(url)

	# parallel
	pool = multiprocessing.Pool(processes=4)
	pool.map(pdf_downloader, urllist)

def pdf_downloader(url):

	output_file = 'pdf'+os.sep+url.split(os.sep)[-1]

	r = requests.get(url, stream=True)
	
	with open(output_file, 'wb') as f:
		f.write(r.content)
	
	print output_file
	return

if __name__ == "__main__":
	main()