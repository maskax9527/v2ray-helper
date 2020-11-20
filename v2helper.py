import requests
import json
import time
import random
import re   
from bs4 import BeautifulSoup

# 加入随机延时
time.sleep(random.randint(1,3))

password = ""
if password == "":
    password = input().strip()
    
def send_wechat(content):
    # title and content must be string.
    sckey = "SCU36037T22f0422808ccaabca3bb2f61044c0bc25c4290cd91060" # your key
    title = "Ypork.v2ray签到通知"                                   
    url = 'https://sc.ftqq.com/' + sckey + '.send'
    data = {'text':title,'desp':content}
    result = requests.post(url,data)
    return(result)    

def get_trafficeinfo_by_lxml():
    url='http://movie.douban.com/top250?format=text'
    contents = requests.get(url)
    print(contents)  
    soup = BeautifulSoup(contents,"html.parser")  
    print("豆瓣电影TOP250" + "\n" +" 影片名              评分       评价人数     链接 ")    
    for tag in soup.find_all('div', class_='info'):    
        m_name = tag.find('span', class_='title').get_text()        
        m_rating_score = float(tag.find('span',class_='rating_num').get_text())          
        m_people = tag.find('div',class_="star")  
        m_span = m_people.findAll('span')  
        m_peoplecount = m_span[3].contents[0]  
        m_url=tag.find('a').get('href')  
        print( m_name+"        "  +  str(m_rating_score)   + "           " + m_peoplecount + "    " + m_url )   
    
def main():
    s = requests.session()
    s.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    url0 = f'https://forever.ypork.com/auth/login'
    r = requests.get(url0, timeout=15)
    fromdata = {
        'email':'1098978935@qq.com',
        'passwd': password
    }
    headers0 = {
        'origin': 'https://forever.ypork.com',
        'referer' : 'https://forever.ypork.com/auth/login'
    }
    r0 = s.post(url0, data=fromdata, headers=headers0, timeout=15)
    if r0.status_code == 200:
        t = json.loads(r0.text)
        lm = t['msg']
        print(t['msg'])
    else:
        send_wechat("登录失败")
            
    url2 = f"https://forever.ypork.com/user/checkin"

    r2 = s.post(url2, timeout=15)
    r2.raise_for_status()
    t = json.loads(r2.text)
    if t["msg"]:
        print(t["msg"])
        get_trafficeinfo_by_lxml()
        send_wechat("登录信息："+lm + "\n签到信息："+t['msg'])
    else:
        print("Error")
        send_wechat("错误信息："+t['msg'])
        exit(100)

if __name__ == "__main__":
    main()
