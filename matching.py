#!/usr/bin/python
import os
cat_prefix = "/Users/gonzales/enron/enron_with_categories/"
maildir_prefix="/Users/gonzales/enron/enron_experiment/"
cat_md5s_file=open('cat_md5s','r')
cat_ids_file=open('cat_emails','r')
cat_filenames_file=open('cat_emails2','r')
md5s_file=open('md5s','r')
ids_file=open('emails','r')
filenames_file=open('emails2','r')
cat_hash_md5={}
cat_hash_id={}
matches_hash={}
counts_hash={}

for line in cat_md5s_file:
	line=line.rstrip('\n')
	parts=line.split()
	#parts[3] is the hash
	filename=cat_filenames_file.readline()
	filename=filename.rstrip('\n')
	cat_hash_md5[parts[3]]=filename
	cat_hash_id[cat_ids_file.readline().rstrip('\r\n')]=filename

for line in md5s_file:
	line=line.rstrip('\n')
	parts=line.split()
	#parts[3] is the hash
	filename=filenames_file.readline()
	filename=filename.rstrip('\n')
	message_id=ids_file.readline().rstrip('\r\n')	
	if (cat_hash_md5.has_key(parts[3])):
		if matches_hash.has_key(cat_hash_md5[parts[3]]):
			matches_hash[cat_hash_md5[parts[3]]]+=filename
		else:
			matches_hash[cat_hash_md5[parts[3]]]=filename
		if counts_hash.has_key(cat_hash_md5[parts[3]]):
			counts_hash[cat_hash_md5[parts[3]]]+=1
		else:
			counts_hash[cat_hash_md5[parts[3]]]=1
	elif cat_hash_id.has_key(message_id):
		if matches_hash.has_key(cat_hash_id[message_id]):
			matches_hash[cat_hash_id[message_id]]+=filename
		else:
			matches_hash[cat_hash_id[message_id]]+=filename
		if counts_hash.has_key(cat_hash_id[message_id]):
			counts_hash[cat_hash_id[message_id]]+=1
		else:
			counts_hash[cat_hash_id[message_id]]=1
	else:
		continue

for key in counts_hash:
	if counts_hash[key]>1:
		print key +" "+ str(counts_hash[key])
		print key + " " + matches_hash[key]

for key in matches_hash:
	#print matches_hash[key]
	#print key
	#problems
	#currently does not create directories under the username in enron_experiment
	#needs to copy both the .cats and the .txt file from the enron_with_cats directory
	#os.system("diff "+ "enron_with_categories/"+key +  " " + matches_hash[key])
	foo=matches_hash[key].split("/")
	foo2=key.split("/")
	#print foo[1]
	#print foo2[2]
	prefix =foo2[2].split(".")
	os.system("mkdir -p enron_experiment/" + foo[1]+"/"+foo2[1])
	os.system(" cp  /Users/gonzales/enron/enron_with_categories/" + foo2[1]+"/"+prefix[0]+".*"+" enron_experiment/"+foo[1]+"/"+foo2[1]+"/")
	
