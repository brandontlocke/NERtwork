#!/bin/sh

echo "doc,entity,type,count" > entities.csv

for file in *.txt

do

nertext=$(stanford-ner-2018-02-27/ner.sh $file)

echo $nertext | egrep -o "(([[:alnum:]]|\.)+/ORGANIZATION([[:space:]]|$))+" | sed 's/\/ORGANIZATION//g' | sort | uniq -c | awk -v name=${file##*/} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "organization" ","; printf $1;  print ""}' >> entities.csv

echo $nertext | egrep -o "(([[:alpha:]]|\.)*/PERSON([[:space:]]|$))+" | sed 's/\/PERSON//g' | sort | uniq -c | awk -v name=${file##*/} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "person" ","; printf $1;  print ""}' >> entities.csv

echo $nertext | egrep -o "(([[:alnum:]]|\.)*/LOCATION[[:space:]](,[[:space:]])?)+" | sed 's/\/LOCATION//g' | sort | uniq -c | awk -v name=${file##*/} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "location" ","; printf $1;  print ""}' >> entities.csv

done
