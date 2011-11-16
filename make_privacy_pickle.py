#!/usr/bin/python
import sys
import os
import subprocess
import pickle

output = subprocess.Popen("cat queries/"+sys.argv[1]+"/privacy/*.files",shell=True, stdout=subprocess.PIPE).stdout
outfile = open("queries/"+sys.argv[1]+"/privacy/privacy_pickle","wb")
privacy= set()
for line in output:
	line=line.rstrip("\n")
	privacy.add(line)

print privacy
pickle.dump(privacy,outfile)
outfile.close()
