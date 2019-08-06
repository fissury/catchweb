'''
写一个网站爬虫，可以爬取到前10页的ip，地理位置，端口号
'''

import urllib.request
import requests
import re
import pymysql
import time

def write_data(list, num):
    # num控制把爬取到的ip写到文本中
    for i in range(num):  
        u = list[0]
        with open('C:\\Users\\Shinelon\\Desktop\\a.txt', 'a') as data:
            print(u, file=data)
def isLive():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]
    #这个是你放网址的文件名，改过来就可以了
    file = open('C:\\Users\\Shinelon\\Desktop\\a.txt')
    lines = file.readlines()
    aa=[]
    for line in lines:
        temp=line.replace('\n','')
        aa.append(temp)
    print(aa)
    print('开始检查：')
    count= 0  # 计算txt中网站的数量
    newfile = open("C:\\Users\\Shinelon\\Desktop\\b.txt","a")
    for a in aa:
        tempUrl = a
        try :
            opener.open(tempUrl)
            print(tempUrl+'没问题')
            newfile.write(a+"\n")
            return True
        except urllib.error.HTTPError:
            print(tempUrl+'=访问页面出错')
            time.sleep(2)
            return False
        except urllib.error.URLError:
            print(tempUrl+'=访问页面出错')
            time.sleep(2)
            return False
        time.sleep(0.1)
    newfile.close()


#连接数据库
db = pymysql.connect("localhost","root","root","testdb" )
cursor = db.cursor()
count = 0
#循环页数，将每一页的ip，端口号等信息存入文件
for i in range(1,10):
    url = 'http://www.89ip.cn/'
    #观察网站地址随页数变化的规律为http://www.89ip.cn/index_123456789.html
    url=url+'index_'+str(i)+'.html'
    response = requests.get(url)
    HTML = response.text
    #利用正则表达式匹配ip地址
    pattern= re.compile(r'(((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3})')
    #利用正则表达式匹配端口号
    compile_1 = re.compile(r'\s+(\d{3,6})\s')
    #利用正则表达式匹配地区信息    
    compile_2 = re.compile(r'\s+([\u4e00-\u9fa5]{1,9})\s?(?:省|新疆|内蒙古|西藏|宁夏|市|县|区])')
    result = pattern.findall(HTML)  
    res1 = compile_1.findall(HTML)
    res2 = compile_2.findall(HTML)
    for ip_ in result:
        write_data(ip_,len(result)) 
        if isLive :
            sql = "INSERT INTO test (ip,port,place) VALUES ('%s','%s','%s')" %(ip_[0],res1[0],res2[0])
            print(sql)
            cursor.execute(sql)
        else:
            count += 1
print('共有%d个网站无法访问，请在b.txt中检查失效网站'%count)
db.close()

# 使用cursor()方法获取操作游标 