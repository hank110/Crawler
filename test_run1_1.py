#-*-coding:utf-8-*-
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
import json
import re
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
browser.get('http://s.weibo.com/weibo/%25E9%259F%25A9%25E5%259B%25BD?topnav=1&wvr=6&b=1')

try:
    element = ui.WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "S_weibo")))
finally:

    # denoting xpath for necessary componenets for contents of interest
    elements = browser.find_elements_by_xpath(".//p[@class='comment_txt']")
    name = browser.find_elements_by_xpath(".//div[@class='feed_content wbcon']/a[1]")
    num_likes = browser.find_elements_by_xpath(".//span[@class='line S_line1']")
    time = browser.find_elements_by_xpath(".//div[@class='feed_from W_textb']/a[1]")
    test = browser.find_elements_by_xpath(".//div[@class='feed_from W_textb']")
    cellphone = browser.find_elements_by_xpath(".//a[@rel='nofollow']")
           
    # printing out time
    # refering tweet = no, related article = no
    for i in range(0, len(time)):
        if not str(time[i].get_attribute("title")):
            print "0"
        else:
            print str(time[i].get_attribute("title"))
            
    for i in range(0, len(test)):
        tt = test[i].text
        print tt

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
    indices = [i for i, x in enumerate(num_elements) if x == '\xe5\x88\x86\xe4\xba\xab']
    del num_elements[indices[0]:indices[-1]+2]
     
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
        print str(name[i].get_attribute("nick-name").encode('utf-8'))

    # crawling text (tweets in weibo)
    # refering tweet = yes, related article = no
    for i in range(0,len(elements)):
        text_elements = elements[i].text
        print text_elements