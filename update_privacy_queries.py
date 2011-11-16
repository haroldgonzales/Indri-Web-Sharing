#!/usr/bin/python
import sys
import os
import subprocess

output = subprocess.Popen("find queries/ -mindepth 3 -iname \"*.parameters\"",shell=True, stdout=subprocess.PIPE).stdout
for line in output:
	print line
	line=line.rstrip("\n")
	parts = line.split("/")
	user=parts[1]
	query=((parts[3].split("."))[0]).replace('_',' ')
	print user
	print "./make_stored_query.py "+user+" "+"\""+query+"\""+" 1"
	subprocess.call("./make_stored_query.py "+user+" "+"\""+query+"\""+" 1",shell=True)	
