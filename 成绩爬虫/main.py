from selenium import webdriver
import time
import json
from bs4 import BeautifulSoup, element
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os,sys
import hashlib
import base64
from re import match
from sendmail import sendmail

delay = 10
username = ""#你的用户名
password = ""#你的密码
yourmail = ''
#启动chromedriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1920x1080')
# 创建 WebDriver 对象，指明使用chrome浏览器驱动
#driver = webdriver.Chrome(executable_path='d:\selenium\chromedriver.exe',chrome_options = options) #linux版本，无图形
driver = webdriver.Chrome('d:\selenium\chromedriver.exe')#将路径改为自己的chromedriver路径

def selfclick(xpath,driver=driver):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        temp = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();", temp)
        driver.switch_to.window(driver.window_handles[-1])
    except:
        return "出错，未定位到元素"
def selfinput(xpath,input_element,driver=driver):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.find_element_by_xpath(xpath).send_keys(input_element)
    except:
        return "出错，未定位到元素"
def findresult():
    driver.get("http://ehall.xjtu.edu.cn/new/index.html")
    #登录
    selfclick("//*[@id='ampHasNoLogin']")
    selfinput("//*[@id='form1']/input[1]",username)
    selfinput("//*[@id='form1']/input[2]",password)
    selfclick("//*[@id='account_login']")

    #进入成绩查询界面
    selfclick("//*[@id='widget-recommendAndNew-01']/div[1]/widget-app-item[3]/div/div/div[2]/div[1]")
    driver.switch_to.frame(driver.find_element_by_xpath("//*[@id='thirdpartyFrame']"))
    selfclick("//*[@id='12aa5b5d-3791-4a69-8fda-6e1768da4d97']")
    driver.switch_to.frame(driver.find_element_by_xpath("//*[@id='thirdpartyFrame']"))
    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pinnedtabledqxq-index-table"]/tbody')))
    driver.quit()
    return element
def soupin(element):
    soup = BeautifulSoup(element.get_attribute("outerHTML"))
    with open('result.txt','w',encoding='utf-8') as f:
        f.write(",".join(["课程名","总成绩","期末成绩","平时成绩"])+'\n')
        for i in soup.find_all('a'):
            f.write(",".join([i.attrs['data-kcm'],i.attrs["data-zcj"],i.attrs["data-qmcj"],i.attrs["data-pscj"]])+'\n')

def check():
    with open('history.txt','r+',encoding='utf-8') as f1:
        s1 = [i[:-1].split(',') for i in f1.readlines()]
        with open('result.txt','r+',encoding='utf-8') as f2:
            s2 = [i[:-1].split(',') for i in f2.readlines()]
            result=''
            for i in s2:
                result =result+'<br><br>'+ '/'.join(i)
            if len(s1)==len(s2):
                print("暂无成绩更新")
            elif len(s1)<len(s2):
                f1.seek(0)
                f1.truncate()
                f2.seek(0)
                f1.write(f2.read())
                sendmail(yourmail,'成绩更新',result,'html')
            else:
                sendmail(yourmail,'查询出错,成绩数据小于原定集合',result,'html')

element = findresult()
soupin(element)
check()