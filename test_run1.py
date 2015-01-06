#-*-coding:utf-8-*-
import requests
import selenium
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import json

browser = webdriver.Chrome()
browser.get('http://s.weibo.com/weibo/%25E9%259F%25A9%25E5%259B%25BD?topnav=1&wvr=6&b=1')

'''
# To check for site connection status
r=requests.get('http://s.weibo.com/weibo/%25E9%259F%25A9%25E5%259B%25BD?topnav=1&wvr=6&b=1')
print r.status_code
print r.encoding
'''

wait = ui.WebDriverWait(browser,30)

# Crawling the feed
elements = browser.find_elements_by_xpath(".//p[@class='comment_txt']")
for i in range(0,len(elements)):
    text_elements = elements[i].text
    print text_elements


'''''
from bs4 import BeautifulSoup
import urllib2
opener = urllib2.build_opener()
opener.addheaders = [('User-agent','Mozilla/5.0')]
opener.addheaders = [('Accept-Charset','utf-8')]
test_page = opener.open("http://s.weibo.com/weibo/%25E9%259F%25A9%25E5%259B%25BD?topnav=1&wvr=6&topsug=1")
test_soup = BeautifulSoup(test_page.read())
contents = test_soup.select("p.comment_txt")
print test_soup
'''''