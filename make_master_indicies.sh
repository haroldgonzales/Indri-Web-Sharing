#!/bin/bash

cd enron_experiment
$(rm -r *.index)
for i in $(ls)
do 
	echo $i
	echo $(IndriBuildIndex -corpus.path=$i -corpus.class=text -baseline=tfidf -memory=1g -index=$i.index)
done
