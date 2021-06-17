# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 01:26:13 2021

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

df = pd.DataFrame(columns=['Title', 'Author', 'Link','GenreList',
                        'Description','Rev5-1','Rev5-2','Rev5-3','Rev5-4','Rev5-5',
                        'Rev4-1','Rev4-2','Rev4-3','Rev4-4','Rev4-5',
                        'Rev3-1','Rev3-2','Rev3-3','Rev3-4','Rev3-5'])
try:
    morelink = driver.find_element_by_xpath("//*[@id='descriptionContainer']")
    morelink.find_element_by_partial_link_text("...more").click()
except NoSuchElementException:
    pass

try:
    morefilter = driver.find_element_by_xpath('//div[@id="reviewControls"]')
    morefilterlink = morefilter.find_element_by_partial_link_text("More filters")
    if morefilterlink.is_displayed():
        print ("yep")
    morefilterlink.click()
    print("this worked")
    ratingclick = driver.find_element_by_xpath('//div[@class="borderCenter"]')
    if ratingclick.is_displayed():
        print("this works")
    ratingoptions = ratingclick.find_elements_by_xpath("//*[@href]")
    ratingsavail = ratingclick.find_element_by_partial_link_text("5").click()
    print("yes this works")
except NoSuchElementException:
    print("oh no")
    
time.sleep(10)
i = 0
reviewarray = []
for i in range(0,5):
    review = driver.find_element_by_xpath('//div[@class="reviewText stacked"]')
    try:
        revbutton = review.find_element_by_partial_link_text("...more").click()
    except NoSuchElementException:
        pass
    reviewarray.append(review.text.replace('\n', ' ').replace('(less)', '').replace("\\", " "))
    i = i + 1

print(reviewarray)

list = [driver.find_element_by_xpath('//h1[@class="gr-h1 gr-h1--serif"]').text,
        driver.find_element_by_xpath("//*[@id='description']").text.replace('\n', ' ').replace('(less)',''),
        driver.current_url]

list.append(reviewarray)