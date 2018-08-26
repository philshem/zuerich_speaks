## Text mining 100+ years of Kanton Zürich's referenda and initiatives
[TWIST2018 project](http://hack.twist2018.ch/project/15)

### team
+ [peter moser](https://twitter.com/peterjamoser)\*
+ [philip shemella](https://twitter.com/philshem)
+ [martin holub](https://twitter.com/holub_martin)

\*Peter has some nice papers with previous research

+ https://statistik.zh.ch/content/dam/justiz_innern/statistik/Publikationen/statistik_info/si_2016_04_abstimmungen_uebersicht_2010_2016.pdf

### main data sources:

+ https://opendata.swiss/de/dataset/abstimmungsarchiv-des-kantons-zurich

+ Kantonal level CSV contains URLs to machine-readable pdf voting information

+ Gemeinde level CSV contains per-Gemeinde historical voting records

+ CSVs are joined by unique vote ID (STAT_VORLAGE_ID)

+ PDF are converted to TXT via pdftotext and can be joined to CSV files by field ABSTIMMUNGSTAG


### using the code and data
(mostly python 2.7 or bash)

+ [get_pdfs.py](https://github.com/philshem/zuerich_speaks/blob/master/get_pdfs.py) scrapes the URLs from the Kantonal CSV file and saves them locally. (Actually we got the PDFs from the organizers on a usb stick, because the scraper was getting IP blocked.) Note that the files Bundesamt.pdf are not URL linked in the CSV files.

+ [convert_pdf_to_txt.sh](https://github.com/philshem/zuerich_speaks/blob/master/convert_pdf_to_txt.sh) loops over the PDFs and converts them to TXT with [pdftotext](https://en.wikipedia.org/wiki/Pdftotext).

+ [read_txt.py](https://github.com/philshem/zuerich_speaks/blob/master/read_txt.py) reads the individual TXT files, cleanups up the text a bit, and writes a CSV file with some keys for joining later: full_text.csv ([zipped](https://github.com/philshem/zuerich_speaks/blob/master/full_text.csv.zip)).

+ [vote_mapping.py](https://github.com/philshem/zuerich_speaks/blob/master/vote_mapping.py) (_experimental_) reads the combined text from full_text.csv, and also the metadta from the Kantonal CSV file. It attemps to split the TXT file into multiple elements, one for each ballot measure, using some file-specific some keywords. The code then maps based on the rank of this split array. Output file is [full_text_mapped.csv](https://github.com/philshem/zuerich_speaks/blob/master/full_text_mapped.csv).

+ [sentiment.py](https://github.com/philshem/zuerich_speaks/blob/master/sentiment.py) reads full_text_mapped.csv and calculates the polarity (-1,1), the subjectivity (0,1) with [textblob_de](https://github.com/markuskiller/textblob-de) and the [readability](https://github.com/philshem/zuerich_speaks/blob/master/text_complexity.md#readability-package). Output file is [full_text_mapped_sentiment.csv](https://github.com/philshem/zuerich_speaks/blob/master/full_text_mapped_sentiment.csv), and the three scores are added as the last 3 columns.

![voting](https://static.independent.co.uk/s3fs-public/thumbnails/image/2015/09/25/20/suffragette.jpg?w600)

