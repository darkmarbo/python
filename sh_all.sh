#!/bin/sh

#####    1. 脚本变量解析 
####  ./sh_all.sh   --lm ch.arpa --order 4 --log  aaa  bbb
#
####    $1 $2 通过shift移动之后 就变成后面的变量了 
#for x in `seq 2`;do
#    [ "$1" == "--lm" ] && lm_name=$2 && shift 2; 
#    [ "$1" == "--order" ] && order=$2 && shift 2;
#    [ "$1" == "--log" ] && log_flag=true && shift;
#done
#
#echo "--lm = ${lm_name}"
#echo "--order = ${order}"
#echo "--log_flag = ${log_flag}"
#
#### 此时的 $# 为最终剩余的 变量 所以未匹配的变量要放到最后  
#if [ $# != 2 ];then
#    echo "usage: $0 [options]  <argv1> <argv2> "
#    echo "e.g. : $0 argv1  argv2 "
#    echo "Options :"
#    echo "--lm          # 指定语言模型的path"
#    echo "--order       # 指定语言模型的阶数"
#    exit 1;
#fi
#
#echo "argv1=${1}    argv2=${2}"

####     2. PATH 配置 
#[ -f path.sh ] && . ./path.sh  && echo "export path.sh ok!";





