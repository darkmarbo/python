#!/bin/sh -x 

#python3.2 test.py > res.txt

#name=new
#res=${name}.res
#
#rm -rf ${res}
#cat ${name}.list | while read line
#do
#    python3.2 single.py ${line} >> ${res}
#
#done
#
#
#name=peg
#res=${name}.res
#
#rm -rf ${res}
#cat ${name}.list | while read line
#do
#    python3.2 single.py ${line} >> ${res}
#
#done


### 已经代码 得到价值
name=my
res=${name}.res

rm -rf ${res}
cat ${name}.list | while read line
do
    python3 single_my.py ${line} >> ${res}

done




