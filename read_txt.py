#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os

import unicodecsv as csv
import string

def main():
	
	all_bytes = string.maketrans('', '')  # String of 256 characters with (byte) value 0 to 255

	csv_list = []

	csv_list.append(['file_name','ABSTIMMUNGSTAG','full_text'])

	for f in glob.glob('txt'+os.sep+'*.txt'):
#	for f in glob.glob('txt'+os.sep+'19430926_Volksabstimmung.txt'):

		pdf_name = f.replace('txt/','').replace('.txt','')
		dt = pdf_name.split('_')[0]

		# "10.03.1831"
		dt = dt[0:4] + '.' + dt[4:6] + '.' + dt[6:8]

		with open(f,'rb') as t:
			text = t.read()
			text = text.replace('\n',' ').replace('\r',' ').replace('@',' ').replace('|', ' ')


			text = text.translate(all_bytes, all_bytes[:32])  

		csv_list.append([pdf_name+'.pdf',  dt, text])

	#sprint csv_list

	with open('full_text.csv','wb') as aa:
		writer = csv.writer(aa)
		writer.writerows(csv_list)



		#text = textract.process(f)

def read_pdf():
	pass


if __name__ == "__main__":
	main()