# 使用某一个代理是可以的，但是爬取ip地址出现问题，将采用另一种方式
#coding=utf-8 
from selenium import webdriver
import time
import requests
from lxml import etree
from urllib import request
# 打印网页
# from lxml import html
# from html.parser import HTMLParser

def Ip_Is_useable(url):
    request=requests.get(url,proxies=url)
    if request.status_code==200: flag = 1
    else: flag = 0
    return flag

def Get_Ip_Form_66():
    global iplist
    iplist = []
    _headers = {
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
    _cookies = None
    
    for i in range(1,20):
        html1 = requests.get('http://www.66ip.cn/'+str(i)+'.html',headers=_headers) #爬取前200页
        etree_html = etree.HTML(html1.text)
        # tree3 = html.tostring(etree_html,encoding='utf-8').decode('utf-8')
        # print(tree3)
        
        for j in range(2,12):
            ip = etree_html.xpath('//*[@id="main"]/div/div[1]/table/tbody/tr['+str(j)+']/td[1]/text()')
            port=etree_html.xpath('//*[@id="main"]/div/div[1]/table/tbody/tr['+str(j)+']/td[2]/text()')
            url="http://"+str(ip)+":"+str(port)
            if(Ip_Is_useable(url)): iplist.append(url)
        
def Change_The_Time_Type(Video_Time):
    Digital_Video_Time = time.strptime(Video_Time, "%M:%S")
    Total_Second = Digital_Video_Time.tm_min*60+Digital_Video_Time.tm_sec
    return Total_Second

def Auto_Like_Your_Video(url):
    # 使用代理ip
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--proxy-server="+url)# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
    driver = webdriver.Chrome(options=chromeOptions)
    
    # 打开视频播放页
    driver.get("https://b23.tv/RgeqHr")
    time.sleep(1)
    
    # 获取视频时长
    Video_Time = driver.find_element_by_xpath("//div[@name='time_textarea']/span[3]").text
    Total_Second = Change_The_Time_Type(Video_Time)
    
    # 两倍速
    element=driver.find_element_by_xpath("//button[@class='bilibili-player-video-btn-speed-name']")
    webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
    element=driver.find_element_by_xpath("//ul[@class='bilibili-player-video-btn-speed-menu']/li[1]")
    webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
    
    # 观看视频
    element=driver.find_element_by_xpath("//button[@class='bilibili-player-iconfont bilibili-player-iconfont-start']")
    webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
    time.sleep(Total_Second/2)
    
    # 三连
    # driver.find_element_by_xpath("//div[@class='ops']/span[1]").click()
    # driver.find_element_by_xpath("//div[@class='ops']/span[2]").click()
    # driver.find_element_by_xpath("//div[@class='coin-bottom']/span[1]").click()
    # driver.find_element_by_xpath("//div[@class='ops']/span[3]").click()
    # driver.find_element_by_xpath("//span[@class='fav_title']").click()
    # driver.find_element_by_xpath("//button[@class='btn submit-move']").click()
    time.sleep(2)

if __name__ == "__main__":
    
    Get_Ip_Form_66()

    for url in iplist:
        Auto_Like_Your_Video(url)
    
