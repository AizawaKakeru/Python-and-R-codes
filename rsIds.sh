#!/bin/bash

while read marker
do

rs=`curl -L -s "https://www.ncbi.nlm.nih.gov/snp/?term=$marker" | grep -oh 'rs[0-9]\+' | head -n1`
echo $marker $rs >> rsids.txt

done < markers.txt
