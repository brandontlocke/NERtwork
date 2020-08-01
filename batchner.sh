#!/bin/sh
os='unix'
lang='eng'
dir=''
nerdir='../stanford-ner/'
while getopts 's:l:d:n:' options; do
  case "${options}" in
    s)
      if ! [[ $OPTARG =~ ^(win|unix)$ ]]; then 
        echo "-s flag not recognized. Options are 'unix' or 'win'"
        exit 0; 
      else 
        os="${OPTARG}"; fi
      ;;
    l)
      if ! [[ $OPTARG =~ ^(eng)$ ]]; then 
        echo "-l flag not recognized. Options are 'eng'"
        exit 0; 
      else 
        lang="${OPTARG}"; fi
      ;;

    n)
      nerdir="${OPTARG}"
      echo "looking for stanford-ner at $nerdir"
      ;;  

    d)
      dir="${OPTARG}"
      echo "looking for text files in $dir"
      ;;
    ?)
      echo "script usage: $(basename $0) [-o] [-l] [-d]" >&2
      exit 1
      ;;
  esac
done

if [[ $os =~ ^(unix)$ ]]; then
    echo "doc,entity,entityType,count" > entities.csv
    for file in $dir*.txt
    do
    nertext=$(${nerdir}ner.sh $file)
    echo $nertext | egrep -o "(([[:alnum:]]|\.)+/ORGANIZATION([[:space:]]|$))+" | sed 's/\/ORGANIZATION//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "organization" ","; printf $1;  print ""}' >> entities.csv
    echo $nertext | egrep -o "(([[:alpha:]]|\.)*/PERSON([[:space:]]|$))+" | sed 's/\/PERSON//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "person" ","; printf $1;  print ""}' >> entities.csv
    echo $nertext | egrep -o "(([[:alnum:]]|\.)*/LOCATION[[:space:]](,[[:space:]])?)+" | sed 's/\/LOCATION//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "location" ","; printf $1;  print ""}' >> entities.csv

    done
    fi

if [[ $os =~ ^(win)$ ]]; then
    echo "doc,entity,entityType,count" > entities.csv
    for file in $dir*.txt
    do
    nertext=$(java -mx600m -cp ${nerdir}stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ${nerdir}classifiers/english.all.3class.distsim.crf.ser.gz -textFile $file)
    echo $nertext | egrep -o "(([[:alnum:]]|\.)+/ORGANIZATION([[:space:]]|$))+" | sed 's/\/ORGANIZATION//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "organization" ","; printf $1;  print ""}' >> entities.csv
    echo $nertext | egrep -o "(([[:alpha:]]|\.)*/PERSON([[:space:]]|$))+" | sed 's/\/PERSON//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "person" ","; printf $1;  print ""}' >> entities.csv
    echo $nertext | egrep -o "(([[:alnum:]]|\.)*/LOCATION[[:space:]](,[[:space:]])?)+" | sed 's/\/LOCATION//g' | sort | uniq -c | awk -v name=${file%%.*} '{printf name ","; for (i = 2; i < NF; i++) printf $i " "; printf $NF; printf "," "location" ","; printf $1;  print ""}' >> entities.csv

    done
    fi