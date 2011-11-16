#!/usr/bin/python
import sys
import os
import subprocess
import pickle

outfile = open("queries/"+sys.argv[1]+"/privacy/privacy_pickle","rb")
privacy= pickle.load(outfile)

print privacy
outfile.close()
