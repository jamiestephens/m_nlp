# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 12:23:15 2021

@author: Administrator
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import action_chains
from selenium.common.exceptions import NoSuchElementException   
import time
import pandas as pd


URL = 'https://www.goodreads.com/book/show/29579.Foundation'
driver = webdriver.Firefox(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\geckodriver\geckodriver.exe')
driver.minimize_window()
driver.get(URL)
wait = WebDriverWait(driver, 5)
time.sleep(3)
driver.refresh()
driver.refresh()

searchboart = driver.find_element_by_xpath('//div[@class="searchBox searchBox--navbar"]')
inputElement = searchboart.find_element_by_xpath('//*[@class="searchBox__form"]')
inputElement.send_keys('1')
inputElement.send_keys(Keys.ENTER)

class book():
    
    def __init__(self,title,author,link):
        self.title = title
        self.author = author
        self.link = link
    
    def gettitle():
        title = driver.find_element_by_xpath('//h1[@class="gr-h1 gr-h1--serif"]').text
        return title

        
