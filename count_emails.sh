#!/bin/bash

cd enron_experiment
for i in $(ls)
do 
	echo $i
	echo $(find $i -type f|wc -l)
done
