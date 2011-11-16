#!/usr/bin/python
import os
import sys
import subprocess
if(len(sys.argv)!=4):
	sys.exit(1)

os.chdir('/home/gonzales/enron/enron_experiment')
corpus_basedir=os.getcwd()
query_basedir= '/home/gonzales/enron/queries'
print "IndriRunQuery", "-baseline=tfidf", "-index="+sys.argv[1]+".index", "-query=\""+sys.argv[2]+"\""
output = subprocess.Popen("IndriRunQuery -baseline=tfidf -index="+sys.argv[1]+".index -query=\""+sys.argv[2]+"\"",shell=True, stdout=subprocess.PIPE).stdout
files = []
for line in output:
	files.append((line.split())[1])

if not files:
	sys.exit(1)

if sys.argv[3]==str(0):
	new_index = open(query_basedir+"/"+sys.argv[1]+"/"+sys.argv[2].replace(' ','_')+".parameters", 'w')
	file_list = open(query_basedir+"/"+sys.argv[1]+"/"+sys.argv[2].replace(' ','_')+".files", 'w')

if sys.argv[3]==str(1):
	new_index = open(query_basedir+"/"+sys.argv[1]+"/privacy/"+sys.argv[2].replace(' ','_')+".parameters", 'w')
	file_list = open(query_basedir+"/"+sys.argv[1]+"/privacy/"+sys.argv[2].replace(' ','_')+".files", 'w')

print >> new_index, "<parameters>"
for x in files:
	print >> new_index,  "<corpus>"
	print  >> new_index, "<path>"+corpus_basedir+"/"+x+"</path>"
	print  >> file_list, corpus_basedir+"/"+x
	print  >> new_index, "<class>text</class>"
	print  >> new_index, "</corpus>"

print  >> new_index, "<memory>1g</memory>"

if sys.argv[3]==str(0):
	print  >> new_index, "<index>"+query_basedir+"/"+sys.argv[1]+"/"+sys.argv[2].replace(' ','_')+".index</index>"

if sys.argv[3]==str(1):
	print  >> new_index, "<index>"+query_basedir+"/"+sys.argv[1]+"/privacy/"+sys.argv[2].replace(' ','_')+".index</index>"

print  >> new_index, "</parameters>"
new_index.close()
file_list.close()

if sys.argv[3]==str(0):
	subprocess.call("IndriBuildIndex "+query_basedir+"/"+sys.argv[1]+"/"+sys.argv[2].replace(' ','_')+".parameters",shell=True) 

if sys.argv[3]==str(1):
	subprocess.call("IndriBuildIndex "+query_basedir+"/"+sys.argv[1]+"/privacy/"+sys.argv[2].replace(' ','_')+".parameters",shell=True) 

print query_basedir+"/"+sys.argv[1]+"/"+sys.argv[2].replace(' ','_')+".index";
sys.exit(0)
