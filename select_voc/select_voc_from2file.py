# -*- coding: utf-8 -*-
import os
import sys
import string


if len(sys.argv) < 6:
	print "usage: py pplm.dict seg.corpus out.right out.other COUNT\n"
	print "out.right:pplm.dict中的词在seg出现次数大于COUNT \n"
	print "out.right:pplm.dict中的词在seg出现次数小于COUNT \n"
	sys.exit() 

## pplm.dict
f1=open(sys.argv[1],"r")
## seg.corpus
f2=open(sys.argv[2],"r")
## pplm.dict 在seg.corpus中出现次数大于num的
f3=open(sys.argv[3],"w")
f4=open(sys.argv[4],"w")
COUNT=string.atoi(sys.argv[5])
print "COUNT is %d"%(COUNT)


list_line_f1=f1.readlines()
list_line_f2=f2.readlines()
dict1={}
dict2={}

### read pplm.dict file 
for line in list_line_f1:
	if line[-1] == '\n' or line[-1] == ' ':
		line = line[0:len(line)-1]

	if dict1.has_key(line):
		dict1[line] = dict1[line]+1
	else:
		dict1[line]=1

for line in list_line_f2:
	if line[-1] == '\n' or line[-1] == ' ':
		line = line[0:len(line)-1]

	arr=line.split("\t")
	if len(arr) >= 2:
		count=string.atoi(arr[0])
		word=arr[1]
	else:
		count=1
		word=arr[0]
		
	if dict2.has_key(line):
		dict2[word] += count
	else:
		dict2[word] = count

for k in dict1.keys():
	if dict2.has_key(k) and dict2[k] > COUNT:
		f3.write("%d\t%s\n"%(dict2[k],k))
	elif not dict2.has_key(k):
		f4.write("0\t%s\n"%(k))
	else:
		f4.write("%d\t%s\n"%(dict2[k],k))



f1.close()
f2.close()
