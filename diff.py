# -*- coding: utf-8 -*-
import sys
import string

if len(sys.argv)<3:
	print "usage: %s file1 file2"%(sys.argv[0])
	print "file1 is dict.\nfile2 is check"
	sys.exit(0)

f1=open(sys.argv[1])
f2=open(sys.argv[2])
vec_f1=f1.readlines()
vec_f2=f2.readlines()
dict1={}
for line in vec_f1:
	line=line.strip('\r\n')
	dict1[line]=1
for line in vec_f2:
	line=line.strip('\r\n')
	if not dict1.has_key(line):
		print line
	
