# -*- coding: utf-8 -*-
import sys
import string
import commands

if len(sys.argv)<3:
	print "usage: %s word_list dir outfile"%(sys.argv[0])
	sys.exit(0)

f1=open(sys.argv[1])
f_out=open(sys.argv[3],'w')
vec_f1=f1.readlines()

for word in vec_f1:
	word=word.strip('\n\r')
	cmd="grep \" %s \" %s/*|wc -l"%(word,sys.argv[2])
	#print cmd
	(ret,out)=commands.getstatusoutput(cmd)	
	f_out.write("%s\t%s\n"%(out,word))
	f_out.flush()

f1.close()
f_out.close()
