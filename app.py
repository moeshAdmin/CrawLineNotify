import requests, pickle, time, os, random
from bs4 import BeautifulSoup
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import configparser
config = configparser.ConfigParser(interpolation=None)
config.read('config.cfg')

def initProcess():
    try:
        profile_path = 'C:\\Users\\User\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\969sgqz9.python'
        options=Options()
        options.set_preference('profile', profile_path)
        service = Service('geckodriver.exe')

        driver = Firefox(service=service, options=options)
        driver.set_window_position(500, 200) 
        driver.set_window_size(800, 600)
        driver.get('https://approved.tw.landrover.com/approved-vehicles/search/?budget-program%5B%5D=pay&section%5B%5D=41421&order=price&pageId=298702&all-makes=1')
        driver.quit()
    except Exception as e: 
        errorProcess(driver,e,cookieName,source,runType)

def GetData(): #
    global config
    init = config.get('CAR', 'init')
    url = config.get('CAR', 'url')
    
    headers = {}
    cookies = {}

    r = requests.Session()
    res = r.get(init,cookies=cookies, headers=headers)
    res2 = r.get(url,cookies=cookies, headers=headers)
    if 'invalid' in res2.text:
        print('fail')
        exit()

    json = dict(res2.json())
    sCount = str(json['count'])
    print(f"共有"+sCount+"結果")
    for carData in json['vehicles']:
        setStr = carData["link_title"]+"("+carData['model_year']+"款) "+carData['bodystyle']+" "+carData['price_now']+" 里程數:"+carData['mileage']+""
        SendLineNotifiy(setStr)
        time.sleep(5)

def SendLineNotifiy(message):
    global config
    headers = {
        'Authorization': 'Bearer '+config.get('CAR', 'line_token'),
    }
    postData = {
        'message':message
    }
    r = requests.Session()
    res = r.post('https://notify-api.line.me/api/notify',data=postData, headers=headers)
    json = dict(res.json())
    print(json)

initProcess()
GetData()