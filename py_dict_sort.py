
import sys
import os

dic = {'a':31, 'bc':5, 'c':3, 'asd':4, 'aa':74, 'd':0}
dict= sorted(dic.iteritems(), key=lambda d:d[1], reverse = True)
print dict
#print dic.iteritems()

dic = {'a':31, 'bc':5, 'c':3, 'asd':4, 'aa':74, 'd':0}
dict= sorted(dic.iteritems(), key=lambda d:d[0])
print dict
