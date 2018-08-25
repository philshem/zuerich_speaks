text mining 100+ years of Zürich referenda and initiatives

main data source:
+ https://opendata.swiss/de/dataset/abstimmungsarchiv-des-kantons-zurich
+ Kantonal level CSV contains URLs to machine-readable pdf voting information
+ Gemeinde level CSV contains per-Gemeinde historical voting records
+ CSVs are joined by unique vote ID (STAT_VORLAGE_ID)
+ PDF are converted to TXT via pdftotext and can be joined to CSV files by field ABSTIMMUNGSTAG

team: philip shemella, peter moser

![voting](https://static.independent.co.uk/s3fs-public/thumbnails/image/2015/09/25/20/suffragette.jpg?w600)

