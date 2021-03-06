#coding=utf-8

import sys
import urllib
import urllib.request
import re
import random
import time

#抓取所需内容
user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
              'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
              'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']


id=sys.argv[1]
url='http://stock.quote.stockstar.com/'+id+'.shtml'
#print(url);

request = urllib.request.Request( url=url, headers={"User-Agent":random.choice(user_agent)} );

try:       
    response = urllib.request.urlopen(request)
except urllib.error.HTTPError as e:            #异常检测
    print('page=',e.code)
except urllib.error.URLError as e:
    print('page=','',e.reason)


#读取内容
content = response.read().decode('gbk'); 
#print (str(content));

##  class="green">37.45</span><span
##  class="red">146.88</span><span
pattern = re.compile('class="\w+">[0-9\.]*</span><span') 
body = re.findall(pattern, str(content))
#print(body[0]);

pattern = re.compile('class="\w+">([0-9\.]+)</span><span')
stock_page = re.findall(pattern, body[0])      #正则匹配
print(id + "\t" + stock_page[0]);

#stock_total.extend(stock_page)
#每抓一页随机休眠几秒，数值可根据实际情况改动
#time.sleep(random.randrange(8,10))        




##stock_total：所有页面的数据   
#stock_total=[]   
#
#for page in range(1,8):
#
#    url='http://quote.stockstar.com/stock/ranklist_a_3_1_'+str(page)+'.html'
#
#    #随机从user_agent列表中抽取一个元素
#    request = urllib.request.Request( url=url, headers={"User-Agent":random.choice(user_agent)} );
#
#    try:       
#        response = urllib.request.urlopen(request)
#    except urllib.error.HTTPError as e:            #异常检测
#        print('page=',page,'',e.code)
#    except urllib.error.URLError as e:
#        print('page=',page,'',e.reason)
#
#    #读取网页内容
#    content=response.read().decode('gbk')       
#    #打印成功获取的页码
#    print('get page',page)                  
#
#    pattern = re.compile('<tbody[\s\S]*</tbody>') 
#    body = re.findall(pattern,str(content))
#    pattern = re.compile('>(.*?)<')
#
#    #stock_page：某页的数据
#    stock_page = re.findall(pattern,body[0])      #正则匹配
#    stock_total.extend(stock_page)
#    time.sleep(random.randrange(1,4))        #每抓一页随机休眠几秒，数值可根据实际情况改动
#
##删除空白字符
#stock_last=stock_total[:]  #stock_last为最终所要得到的股票数据
#
#for data in stock_total:
#    if data=='':
#        stock_last.remove('')
#
##打印部分结果
#print('代码\t简称\t最新价\t涨跌幅\t涨跌额\t5分钟涨幅')
#for i in range(0,len(stock_last),13):  #原网页有13列数据，所以步长为13
#    print(stock_last[i],'\t',stock_last[i+1],'\t',stock_last[i+2],'\t',stock_last[i+3],'\t',stock_last[i+4],'\t',stock_last[i+5])
#
#






