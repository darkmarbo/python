#!/bin/sh 

if(($#<1));then
    echo "usage: $0 in_file "
    exit 
fi


################################ 0 变量定义 
file=$1
file_tn=${file}.ok.tn_res.txt
file_pros_zip=${file_tn}.zh-pros_res.zip
file_pros=${file}_pros.txt
file_pinyin=${file}_pinyin.txt

ip_A="root@10.10.10.151"
dir_A="/home/szm/cd/ssh"

ip_19="yanfa@10.10.10.19"
dir_19="/home/yanfa/yanqiwei/proj/ProsSP_Final/ProsSP_Script"

ip_27="root@10.10.10.27"
dir_27="/home/szm/ssh"
cmd_tn="/home/yanfa/yanqiwei/proj/TN_Tools/TN_Toolkit_CPP/TN_Tools.sh"
cmd_prosody="/home/yanfa/yanqiwei/proj/ProsSP_Final/ProsSP_Script/zh_pros_predict.sh"

ip_192="root@10.10.10.192"
dir_192="/home/temp"
cmd_pinyin="perl  /home/yanfa/yfhao/mars/dict/util/make_raw_ph.pl "

##################################  1   简体中文-TN  序号55 
#### 把目标机器上的 临时目录清空 
##ssh  -p 22 ${ip_27}  "rm -rf  ${dir_27}/*;"
#
#scp -P 22 ${dir_A}/${file}  ${ip_27}:${dir_27} 
#
#ssh  -p 22 ${ip_27}  "
#
#    cd ${dir_27};
#    ${cmd_tn} ${dir_27}/${file} zh_cn  zh_cn ;
#
#"
#
#rm -rf ${dir_A}/${file_tn}
#scp -P 22 ${ip_27}:${dir_27}/${file_tn}  ${dir_A}/ 
#if [ -f ${dir_A}/${file_tn} ];then
#    echo "${ip_27} TN successed! "
#else
#    echo "${ip_27} TN failed! "
#fi
#
##################################   2    简体中文-韵律标注  序号55 
#### 把目标机器上的 临时目录清空 
##ssh  -p 22 ${ip_27}  "rm -rf  ${dir_27}/*;"
### 上传 file_tn 到   ip_27的dir_27目录下 
#scp -P 22 ${dir_A}/${file_tn}  ${ip_27}:${dir_27} 
#
#ssh  -p 22 ${ip_27}  "
#
#    cd ${dir_27};
#    ${cmd_prosody}  ${dir_27}/${file_tn}  no  no;  
#
#"
#
#### 下载结果 解压  判断结果是否存在  
#scp -P 22 ${ip_27}:${dir_27}/${file_pros_zip}  ${dir_A}/ 
#rm -rf tmp && mkdir -p tmp
#unzip ${file_pros_zip}  -d tmp
#mv tmp/${file_tn}  ${file_pros} 
#rm -rf ${file_pros_zip}
#
#if [ -f ${dir_A}/${file_pros} ];then
#    echo "${ip_27} prosody successed! "
#else
#    echo "${ip_27} prosody failed! "
#fi
#
#
##################################    3   发音预测   序号17  
#
#
#scp -P 22 ${dir_A}/${file_pros}  ${ip_192}:${dir_192} 
#
#ssh  -p 22 ${ip_192}  "
#
#    cd ${dir_192};
#    ${cmd_pinyin} -i ${file_pros}  -o ${file_pinyin} -l zh-cn_pinyin  -m lingua -w 1
#
#"
#scp -P 22 ${ip_192}:${dir_192}/${file}_pinyin*  ${dir_A}/ 
#if [ -f ${dir_A}/${file_pinyin} ];then
#    echo "${ip_192} pinyin successed! "
#else
#    echo "${ip_192} pinyin failed! "
#fi
#
#
####################################   文件分词 
dir_seg=/home/yanfa/yanqiwei/proj/NLPIR/ICTCLAS2014/src/sample/c_seg
cmd_seg="${dir_seg}/handle_file_pos.sh "
scp -P 22 ${dir_A}/${file}  ${ip_27}:${dir_27} 

ssh  -p 22 ${ip_27}  "

    cd ${dir_seg};
    sh ${cmd_seg} ${dir_27}/${file}   ${dir_27} 1 simplified UTF8 ;
    cd -;

"

scp -P 22 ${ip_27}:${dir_27}/${file}  ${dir_A}/${file}.seg 












