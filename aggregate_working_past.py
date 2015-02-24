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

import os
import time
from random import randint

def text_crawler(telements):
    text_holder = []
    for i in range(0,len(telements)):
        text_elements = telements[i].text
        text_holder.append(text_elements)
    return text_holder

def id_crawler(name):
    id_holder = []
    for i in range(0,len(name)):
        if not name[i].get_attribute("nick-name"):
            id_holder.append("None")
            continue
        else:
            id_holder.append(name[i].text)
    return id_holder

def url_crawler(name):
    url_holder = []
    for i in range(0,len(name)):
        if not name[i].get_attribute("href"):
            url_holder.append("None")
            continue
        else:
            url = str(name[i].get_attribute("href"))
            url_holder.append(url)
    return url_holder

''' 
def id_crawler(name):
    id_holder = []
    for i in range(0,len(name)):
        original_id_loc = name[i].find_element_by_xpath(".//a[@class='W_texta W_fb']")
        original_id = original_id_loc.get_attribute("nick-name")
        id_holder.append(original_id)
        try:
            additional_id_loc = name[i].find_element_by_xpath(".//div[@node-type='feed_list_forwardContent']")
            try:
                additional_id_loc_specific = additional_id_loc.find_element_by_xpath(".//a[@class='W_texta W_fb']")
                additional_id = additional_id_loc_specific.text
                id_holder.append(additional_id)
            except NoSuchElementException:
                id_holder.append("Deleted Post")
                continue
        except NoSuchElementException:
            continue
    return id_holder

def url_crawler(name):
    url_holder = []
    for i in range(0,len(name)):
        original_url_loc = name[i].find_element_by_xpath(".//a[@class='W_texta W_fb']")
        original_url = original_url_loc.get_attribute("href")
        url_holder.append(original_url)
        try:
            additional_url_loc = name[i].find_element_by_xpath(".//div[@node-type='feed_list_forwardContent']")
            try:
                additional_url_loc_specific = addtional_url_loc.find_element_by_xpath(".//a[@class='W_texta W_fb']")
                additional_url = additional_url_loc_specific.get_attribute("href")
                url_holder.append(additional_url)
            except NoSuchElementException:
                url_holder.append("Deleted Post")
                continue
        except NoSuchElementException:
        # AttributeError: 'NoneType' object has no attribute 'find_element_by_xpath'    
            continue
    return url_holder
'''
def time_crawler(post_time):
    current_time = datetime.datetime.now()
    time_holder =[]
    for i in range(0, len(post_time)):
        time_retweet = post_time[i].find_element_by_xpath('.//a')
        actual_cell = time_retweet.get_attribute("title")
        if not actual_cell:
            previous_time = time_retweet.text.encode('utf-8')
            # adjusting yue & ri(format done)
            if '\xe6\x9c\x88' in previous_time:          
                previous_time_edited = previous_time.replace("\xe6\x9c\x88", "-")
                previous_time_edited2 = previous_time_edited.replace("\xe6\x97\xa5", " ")
                current_year = "%4d-" % (current_time.year)
                combined_string = current_year + previous_time_edited2
                time_holder.append(combined_string)
            # adjusting jin tian (format done)
            elif '\xe4\xbb\x8a\xe5\xa4\xa9' in previous_time:
                previous_time_edited = previous_time.replace("\xe4\xbb\x8a\xe5\xa4\xa9", "")
                current_ymd = "%4d-%d-%d " % (current_time.year, current_time.month, current_time.day)
                combined_string = current_ymd + previous_time_edited
                time_holder.append(combined_string)        
            # adjusting fen
            elif '\xe5\x88\x86\xe9\x92\x9f\xe5\x89\x8d' in previous_time:
                previous_time_edited = previous_time.replace("\xe5\x88\x86\xe9\x92\x9f\xe5\x89\x8d", "")
                # print previous_time_edited
                time_of_single_tweet = current_time - datetime.timedelta(minutes = int(previous_time_edited))
                time_holder.append(time_of_single_tweet.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                time_holder.append(previous_time)
        else:
            time_holder.append(actual_cell)
    return time_holder
    
def cellphone_crawler(cellphone):
    cell_holder = []
    for i in range(0, len(cellphone)):
        try:
            actual_cell = cellphone[i].find_element_by_xpath('.//a[@rel = "nofollow"]')
            cell = actual_cell.text
            cell_holder.append(cell)
        except NoSuchElementException:
            cell_holder.append("None")
            continue
    return cell_holder

def num_like_crawler(num_likes):
    num_elements = []
    for i in range(0,len(num_likes)):
        num_elements.append(num_likes[i].text.encode('utf-8'))
        try:
            num_elements.remove('\xe6\x94\xb6\xe8\x97\x8f')
        except ValueError:
            continue
    indices = [k for k, s in enumerate(num_elements) if '\xe5\x88\x86\xe4\xba\xab' in s]
    if not indices:
        return num_elements
    else:
        print indices
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

def month_creator():
    month = []
    for i in range(1, 13):
        month_string = str(i)
        if len(month_string) == 1:
            two_digit_month = "0" + month_string
            month.append(two_digit_month)
        else:
            month.append(month_string)
    return month

def time_creator():
    time = []
    for i in range(0, 24):
        time_string = str(i)
        time.append(time_string)
    return time

def date_creator(month):
    date = []
    if month == "02":
        for i in range(1, 29):
            date_string = str(i)
            if len(date_string) == 1:
                two_digit_date = "0" + date_string
                date.append(two_digit_date)
            else:
                date.append(date_string)
        return date
    elif month in ["04", "06", "09", "11"]:
        for i in range(1,31):
            date_string = str(i)
            if len(date_string) == 1:
                two_digit_date = "0" + date_string
                date.append(two_digit_date)
            else:
                date.append(date_string)
        return date
    else:
        for i in range(1,32):
            date_string = str(i)
            if len(date_string) == 1:
                two_digit_date = "0" + date_string
                date.append(two_digit_date)
            else:
                date.append(date_string)
        return date

def create_url_list(month, time):
    total_list = []
    for l in range(0, len(month)):
        d = date_creator(month[l])
        for v in range(0, len(d)):
            for b in range(0, len(time)):
                previous_time = month[l] + "-" + d[v] + "-" + time[b]
                total_list.append(previous_time)
    return total_list

def create_path(root_path, url_list):
    for i in range(0, len(url_list)):
        d = url_list[i].replace("-", " ").split()
        dir_path = root_path + "/" + d[0] + "/" + d[1]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    print "Folder Created Complete"

def get_month(total):
    d = total.replace("-", " ").split()
    return d[0]

def get_date(total):
    d = total.replace("-", " ").split()
    return d[1]    

def main():
    m = month_creator()
    t = time_creator()
    total = create_url_list(m,t)
    # create_path("D:/weibo/2014", total)
    # start from 4 ~ 5
    for i in range(4, len(total)):
        current_time = datetime.datetime.now()
        browser = webdriver.Chrome()
        previous_time = "%s:2014-" %(total[i])
        next_time = "%s&Refer=g" %(total[i+1])
        dir_month = get_month(total[i])
        dir_date = get_date(total[i])
         
        target = "http://s.weibo.com/wb/%25E9%259F%25A9%25E5%259B%25BD&xsort=time&timescope=custom:2014-" + previous_time + next_time
        browser.get(target)
        browser.implicitly_wait(50)
        # time.sleep(20)
        login = browser.find_element_by_xpath('.//a[@node-type="loginBtn"]')
        login.click()
        browser.implicitly_wait(30)
        for handle in browser.window_handles:
            browser.switch_to.window(handle)
        username = browser.find_element_by_xpath(".//input[@tabindex='1']")
        password = browser.find_element_by_xpath(".//input[@tabindex='2']")
        username.send_keys("id")
        password.send_keys("password")
        ok = browser.find_element_by_xpath('.//a[@node-type="submitBtn"]')
        ok.click()
        browser.implicitly_wait(30)
       
        # To check if end reached
        checker = True
        counter = 0
        while(checker == True):
            ran_sec = randint(1, 90)
            print str(ran_sec) + "second waiting"
            time.sleep(ran_sec)
            print "Waiting Completed"
            counter += 1
        
            elements = browser.find_elements_by_xpath(".//p[@class='comment_txt']")
            name = browser.find_elements_by_xpath(".//a[@class='W_texta W_fb']")
            num_likes = browser.find_elements_by_xpath(".//span[@class='line S_line1']")
            post_time = browser.find_elements_by_xpath(".//div[@class='feed_from W_textb']") 
            cellphone = browser.find_elements_by_xpath(".//div[@class='feed_from W_textb']")
            
            print type(elements[0])
            print type(browser)
            
            text = text_crawler(elements)
            id_user = id_crawler(name)        
            url = url_crawler(name)
            posted_time = time_crawler(post_time)
            provider = cellphone_crawler(cellphone)
            num_like_preprocessed = num_like_crawler(num_likes)
            num_like_processed = num_like_separator(numeric_transition(num_like_preprocessed))
        
            print len(num_like_processed)
            print len(text)
            print len(id_user)
            print len(url)
            print len(posted_time)
            print len(provider)
            
            for j in range(0, len(text)):
                entry = {}  
                entry['ID'] = id_user[j].encode('utf-8')
                entry['Text'] = text[j].encode('utf-8')
                entry['Url'] = url[j]
                entry['Time'] = posted_time[j]
                entry['Number of Response'] = num_like_processed[j]
                entry['Source'] = provider[j].encode('utf-8')
                with codecs.open("D:/weibo/2014/" + dir_month + "/" + dir_date + "/" + "data" + "_" + str(i) + "_" + str(counter) + "_"+ `j` +'.json', 'w', encoding='utf-8') as outfile:
                    try:
                        json.dump(entry, outfile)
                        print "Crawl Complete"
                    except UnicodeDecodeError:
                        continue
                
            try:
                next_button = browser.find_element_by_xpath('.//a[@class="page next S_txt1 S_line1"]')
            except NoSuchElementException:
                print "Crawling Finished"
                checker = False
                continue
            next_button.click()
            print "Next Page"
            browser.implicitly_wait(30)
               
if __name__ == "__main__":
    main()