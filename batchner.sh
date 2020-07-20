#!/bin/sh
echo "doc,entity,entityType,count" > entities.csv
for file in *.txt
do
############################
#If you're using Windows, delete the # from the start of line 8 and add a # to the start of line 9
############################
#nertext=$(java -mx600m -cp ../stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ../stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz -textFile $file)
nertext=$(../stanford-ner/ner.sh $file)

echo $nertext | egrep -o "(([[:alnum:]]|\.)+/ORGANIZATION([[:space:]]|$))+" | sed 's/\/ORGANIZATION//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "organization" ","; printf $1;  print ""}' >> entities.csv
echo $nertext | egrep -o "(([[:alpha:]]|\.)*/PERSON([[:space:]]|$))+" | sed 's/\/PERSON//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "person" ","; printf $1;  print ""}' >> entities.csv
echo $nertext | egrep -o "(([[:alnum:]]|\.)*/LOCATION[[:space:]](,[[:space:]])?)+" | sed 's/\/LOCATION//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "location" ","; printf $1;  print ""}' >> entities.csv

done
