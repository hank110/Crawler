#-*-coding:utf-8-*-
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
import json

browser = webdriver.Chrome()
browser.get('http://s.weibo.com/weibo/%25E9%259F%25A9%25E5%259B%25BD?topnav=1&wvr=6&b=1')
# wait = ui.WebDriverWait(browser,5000)

try:
    element = ui.WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "S_weibo")))
finally:

# Crawling the feed & ID
    elements = browser.find_elements_by_xpath(".//p[@class='comment_txt']")
    name = browser.find_elements_by_xpath(".//a[@class='W_texta W_fb']")
    for i in range(0,len(name)):
        name_elements = name[i].text
        print name_elements
    
    for i in range(0,len(elements)):
        text_elements = elements[i].text
        print text_elements    
        