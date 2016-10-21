#!/bin/sh

#python select_voc_from2file.py  pplm.dict voc.all.ok sel.then20 ttt 20
#sort -n -r sel.then20 > sel.then20.sort

head -80000 voc.all.ok > out.voc
head -140000 sel.then1.sort > out.sel
cat out.voc out.sel  pplm.dict.single > out.cat.22w
awk -F"\t" '{print $2}' out.cat.22w |sort|uniq|sort > out.cat.22w.uniq
##awk '{print NR"\t"$0}' voc-and-sel.30w.uniq > pplm.dict.out

