#-*- coding: utf-8 -*-

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
import json
import re
from selenium.common.exceptions import NoSuchElementException
import datetime
from datetime import timedelta
import sys

# to resolve encoding issue
reload(sys)
sys.setdefaultencoding('utf-8')

browser = webdriver.Chrome()
browser.get('http://s.weibo.com/weibo/%25E9%259F%25A9%25E5%259B%25BD&b=1&page=1')


try:
    element = ui.WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "S_weibo")))
finally:
    # denoting xpath for necessary componenets for contents of interest
    elements = browser.find_elements_by_xpath(".//p[@class='comment_txt']")
    name = browser.find_elements_by_xpath(".//a[@class='W_texta W_fb']")
    num_likes = browser.find_elements_by_xpath(".//span[@class='line S_line1']")
    time = browser.find_elements_by_xpath(".//div[@class='feed_from W_textb']/a[1]")
    test = browser.find_elements_by_xpath(".//div[@class='feed_from W_textb']")
    cellphone = browser.find_elements_by_xpath(".//a[@rel='nofollow']")
    
    elements_container = []
    name_container = []
    num_likes_container = []
    time_container = []
    cellphone_container = []
    
    current_time = datetime.datetime.now()
    
    # url of each user acquired
    for i in range(0,len(name)):
        url = str(name[i].get_attribute("href"))
        if 'http://weibo.com/p/' in url:
            continue
        else:
            print url
    
                    
    for i in range(0, len(test)):
        tt = test[i].text
        splited = tt.split(" ")
        time_part = splited[0].encode('utf8')
        if "分" in time_part:
            position = time_part.index('分')
            minutedelta = int(time_part[0:position])
            time_of_single_tweet = current_time - datetime.timedelta(minutes = minutedelta)
            print time_of_single_tweet.strftime("%Y-%m-%d %H:%M:%S")
        elif "秒" in time_part:
            position = time_part.index('秒')
            seconddelta = int(time_part[0:position])
            time_of_single_tweet = current_time - datetime.timedelta(seconds = seconddelta)
            print time_of_single_tweet.strftime("%Y-%m-%d %H:%M:%S")
        elif "月" in time_part:
            position1 = int(time_part.index('月'))
            position2 = int(time_part.index('日'))
            month = int(time_part[0:position1])
            day = int(time_part[position1+3:position2])
            print "%d-%d-%d %s" % (current_time.year, month, day, splited[1])
        elif "今天" in time_part:
            print "%d-%d-%d %s" % (current_time.year, current_time.month, current_time.day, splited[1])
        else:
            print time_part + " " + splited[1]
            
          
    # refering tweet = yes, related article = no
    for i in range(0, len(cellphone)):
        cell = cellphone[i].text
        print cell    
        
    # to get numbers of retweet, comment, likes, respectively
    # refering tweet = yes, related article = no
    num_elements =[]
    for i in range(0,len(num_likes)):
        num_elements.append(num_likes[i].text.encode('utf-8'))
        try:
            #to remove unnecessary crawled element that denotes "favorites"
            num_elements.remove('\xe6\x94\xb6\xe8\x97\x8f')
        except ValueError:
            continue
        
    # to find the indices of unnecessary elements(likes & share menues and the number of likes for "related articles)
    indices = [i for i, s in enumerate(num_elements) if '分享' in s]
    starting_position = indices[0]
    del num_elements[starting_position:starting_position+6]
     
    final_num_elements =[]
    for i in range(0, len(num_elements)):
        # getting rid of characters within the elements in the list
        # because current form = XX30
        only_number = re.sub("[^0-9]", "", num_elements[i])
        final_num_elements.append(only_number)
        # empty value indicates 0 likes/comments/retweets
        if(final_num_elements[i] == ""):
            final_num_elements[i] = 0
    print final_num_elements
    
    # crawling IDs
    # refering tweet = yes, related article = no
    for i in range(0,len(name)):
        if name[i].get_attribute("nick-name") is None:
            continue
        else:
            print str(name[i].text.encode('utf-8'))
            
    # crawling text (tweets in weibo)
    # refering tweet = yes, related article = no
    for i in range(0,len(elements)):
        text_elements = elements[i].text
        print text_elements