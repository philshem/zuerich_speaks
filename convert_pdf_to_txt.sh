
folder=pdf/

for f in $folder/*.pdf ; do

	pdftotext $f
	echo $f

done

mv $folder/*.txt txt/