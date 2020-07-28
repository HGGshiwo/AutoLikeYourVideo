#coding=utf-8 
from selenium import webdriver
from bs4 import BeautifulSoup  
from urllib import request
import time
import requests
from urllib import request

def Change_The_Time_Type(Video_Time):
    Digital_Video_Time = time.strptime(Video_Time, "%M:%S")
    Total_Second = Digital_Video_Time.tm_min*60+Digital_Video_Time.tm_sec
    return Total_Second

def get_ip_list(url, headers):  
    web_data = requests.get(url, headers=headers)  
    soup = BeautifulSoup(web_data.text, 'lxml')  
    ips = soup.find_all('tr')  
    ip_list = []  
    for i in range(1, len(ips)):  
        ip_info = ips[i]  
        tds = ip_info.find_all('td') #tr标签中获取td标签数据  
        ip = tds[1].text + ':' + tds[2].text
        ip_list.append(ip)  
    return ip_list  

def Get_Ip_Form_66():
    global ip_list
    ip_list=[]
    global headers
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'www.xicidaili.com',
        'If-None-Match':'W/"b077743016dc54409ebe6b86ba7a869b"',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
    }
    cookies = None
    
    for i in range(1,20):
        url = 'http://www.66ip.cn/'+str(i)+'.html'
        ip_list.append(get_ip_list(url,headers))

def Auto_Like_Your_Video(url):
    try:
        # 使用代理ip
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--proxy-server="+str(url))# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
        driver = webdriver.Chrome(options=chromeOptions)
        
        # 打开视频播放页
        driver.get("https://www.bilibili.com/video/BV1ZZ4y1u7PJ")
        time.sleep(2)
        
        # 获取视频时长
        Video_Time = driver.find_element_by_xpath("//div[@name='time_textarea']/span[3]").text
        Total_Second = Change_The_Time_Type(Video_Time)
        
        # 两倍速
        element=driver.find_element_by_xpath("//button[@class='bilibili-player-video-btn-speed-name']")
        webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
        element=driver.find_element_by_xpath("//ul[@class='bilibili-player-video-btn-speed-menu']/li[1]")
        webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
        
        # 点击播放
        element=driver.find_element_by_xpath("//button[@class='bilibili-player-iconfont bilibili-player-iconfont-start']")
        webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
         
        # 页面最小化
        driver.minimize_window() 
        
        # 看完视频
        time.sleep(Total_Second/2)
        
        # 关闭页面
        driver.close()
    except :
        pass

if __name__ == "__main__":
    Get_Ip_Form_66() # 爬取ip地址
    for url in ip_list:
        Auto_Like_Your_Video(url)
    
