#!/usr/bin/python
import os
import sys
import pickle
import subprocess

if(len(sys.argv)!=3):
	sys.exit(1)

picklefile = open("queries/"+sys.argv[1]+"/privacy/privacy_pickle","rb")
privacy= pickle.load(picklefile)

os.chdir('/home/gonzales/enron/enron_experiment')
corpus_basedir=os.getcwd()
query_basedir= '/home/gonzales/enron/queries'
#print "IndriRunQuery", "-baseline=tfidf", "-index="+sys.argv[1]+".index", "-query=\""+sys.argv[2]+"\""
output = subprocess.Popen("IndriRunQuery -baseline=tfidf -index="+sys.argv[1]+".index -query=\""+sys.argv[2]+"\"",shell=True, stdout=subprocess.PIPE).stdout
files = []
#print privacy
#print "filtered output follows"
for line in output:
	test='/home/gonzales/enron/enron_experiment/'+(line.split())[1]
#	print "test "+test
	if not test in privacy:
		print line.rstrip('\n')

if not files:
	sys.exit(1)

picklefile.close()
