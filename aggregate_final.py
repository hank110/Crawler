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
import codecs

def text_crawler(telements):
    text_holder = []
    for i in range(0,len(telements)):
        text_elements = telements[i].text.encode('utf-8')
        text_holder.append(text_elements)
    return text_holder
    
def id_crawler(name):
    id_holder = []
    for i in range(0,len(name)):
        if name[i].get_attribute("nick-name") is None:
            continue
        else:
            id_holder.append(str(name[i].text.encode('utf-8')))
    return id_holder

def url_crawler(name):
    url_holder = []
    for i in range(0,len(name)):
        url = str(name[i].get_attribute("href"))
        if 'http://weibo.com/p/' in url:
            continue
        elif 'http://weibo.com/' not in url:
            continue
        else:
            url_holder.append(url)
    return url_holder

def time_crawler(time):
    current_time = datetime.datetime.now()
    time_holder =[]
    for i in range(0, len(time)):
        tt = time[i].text
        splited = tt.split(" ")
        time_part = splited[0].encode('utf8')
        if "分" in time_part:
            position = time_part.index('分')
            minutedelta = int(time_part[0:position])
            time_of_single_tweet = current_time - datetime.timedelta(minutes = minutedelta)
            time_holder.append(time_of_single_tweet.strftime("%Y-%m-%d %H:%M:%S"))
        elif "秒" in time_part:
            position = time_part.index('秒')
            seconddelta = int(time_part[0:position])
            time_of_single_tweet = current_time - datetime.timedelta(seconds = seconddelta)
            time_holder.append(time_of_single_tweet.strftime("%Y-%m-%d %H:%M:%S"))
        elif "月" in time_part:
            position1 = int(time_part.index('月'))
            position2 = int(time_part.index('日'))
            month = int(time_part[0:position1])
            day = int(time_part[position1+3:position2])
            if (splited[1] == "来自"):
                hour_min = time_part[position2+1:]
                time_holder.append("%d-%d-%d %s" % (current_time.year, month, day, hour_min))
            else:
                time_holder.append("%d-%d-%d %s" % (current_time.year, month, day, splited[1]))
        elif "今天" in time_part:
            position = int(time_part.index('天'))
            hour_min = time_part[position+1:]    
            time_holder.append("%d-%d-%d %s" % (current_time.year, current_time.month, current_time.day, hour_min))
        else:
            time_holder.append(time_part + " " + splited[1])
    return time_holder

def cellphone_crawler(cellphone):
    cell_holder = []
    for i in range(0, len(cellphone)):
        cell = cellphone[i].text.encode('utf-8')
        cell_holder.append(cell)
    return cell_holder

def num_like_crawler(num_likes):
    num_elements = []
    for i in range(0,len(num_likes)):
        num_elements.append(num_likes[i].text.encode('utf-8'))
        try:
            num_elements.remove('\xe6\x94\xb6\xe8\x97\x8f')
        except ValueError:
            continue
    indices = [i for i, s in enumerate(num_elements) if '分享' in s]
    starting_position = indices[0]
    # print starting_position
    ending_position = indices[-1]
    # print ending_position
    del num_elements[starting_position:ending_position+2]
    return num_elements

def numeric_transition(num_elements):
    final_num_elements = []
    for i in range(0, len(num_elements)):
        only_number = re.sub("[^0-9]", "", num_elements[i])
        final_num_elements.append(only_number)
        if(final_num_elements[i] == ""):
            final_num_elements[i] = 0
    return final_num_elements

def num_like_separator(num_elements):
    new_list = []
    i = 0
    while i < len(num_elements):
        new_list.append(num_elements[i:i+3])
        i += 3
    return new_list
        
def main():
    # to resolve encoding issue
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    browser = webdriver.Chrome()
    browser.get('http://s.weibo.com/weibo/%25E9%259F%25A9%25E5%259B%25BD&b=1&page=1')
    try:
        element = ui.WebDriverWait(browser, 500).until(EC.presence_of_element_located(By.ID, "S_weibo"))
    finally:
        elements = browser.find_elements_by_xpath(".//p[@class='comment_txt']")
        name = browser.find_elements_by_xpath(".//a[@class='W_texta W_fb']")
        num_likes = browser.find_elements_by_xpath(".//span[@class='line S_line1']")
        time = browser.find_elements_by_xpath(".//div[@class='feed_from W_textb']")
        cellphone = browser.find_elements_by_xpath(".//a[@rel='nofollow']")
        
        text = text_crawler(elements)
        id_user = id_crawler(name)
        url = url_crawler(name)
        time = time_crawler(time)
        provider = cellphone_crawler(cellphone)
        num_like_preprocessed = num_like_crawler(num_likes)
        num_like_processed = num_like_separator(numeric_transition(num_like_preprocessed))
        print len(num_like_processed)
        print len(text)
        print len(id_user)
        print len(url)
        print len(time)
        print len(provider)
        
        for i in range(0, len(text)):
            try:
                entry = {}  
                entry['ID'] = id_user[i]
                entry['text'] = text[i]
                entry['url'] = url[i]
                entry['time'] = time[i]
                entry['source'] = provider[i]
                entry['number of response'] = num_like_processed[i]
                print entry
                with codecs.open('data' +`i` +'.json', 'w', encoding = 'utf-8') as outfile:
                    json.dump(entry, outfile)
            except UnicodeDecodeError:
                continue
            
        browser.quit()
        
if __name__ == "__main__":
    main()