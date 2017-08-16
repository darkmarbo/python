# -*- coding: utf-8 -*-
import sys
import string
import re

if len(sys.argv)<3:
	print "usage: %s input_file output_file"%(sys.argv[0])
	sys.exit(0)

f_in=open(sys.argv[1])
f_out=open(sys.argv[2],'w')
dict_in={}

all_line_in=f_in.readlines()
for line in all_line_in:
	vec_word=re.split(' |\n|,|\r|\.|\$|!|-|\'|%|[0-9]|;',line)
	for word in vec_word:
		if word=='':
			continue
		if dict_in.has_key(word):
			dict_in[word]=dict_in[word]+1
		else:
			dict_in[word]=1

for w in dict_in.keys():
	f_out.write("%d\t%s\n"%(dict_in[w],w))

f_in.close()
f_out.close()
	
