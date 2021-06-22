# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 12:26:31 2021

@author: Administrator
"""
from csv import reader
from csv import DictReader
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
import csv
import pathlib

def scrapedata():
    URL = 'https://www.goodreads.com/book'
    driver = webdriver.Firefox(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\geckodriver\geckodriver.exe')
    driver.maximize_window()
    driver.get(URL)
    wait = WebDriverWait(driver, 5)
    time.sleep(3)
    driver.refresh()
    driver.refresh()
    with open('output_for_getting_review.csv', 'r') as read_obj:
        csv_reader = DictReader(read_obj)
        column_names = csv_reader.fieldnames
        i = 1
        
        for row in csv_reader:
            URL = row['search']
            driver.get(URL)
            time.sleep(5)
            copyreviews(driver,URL)
            
            try:
                driver.find_element_by_partial_link_text("next »").click()
                time.sleep(5)
                copyreviews(driver,URL)
                print("Yes 4/5")
            except NoSuchElementException:
                print("Nvm 2/2")
           
            driver.get(URL)  
            i += 1

def copyreviews(driver,url):
    reviewarray = []
    i = 0
    
    reviewbox = driver.find_elements_by_xpath('//div[@class="friendReviews elementListBrown"]')
    size = len(reviewbox)
    print(size)
    for i in range(0,size):
        list= []
        review = driver.find_elements_by_xpath('//div[@class="friendReviews elementListBrown"]')[i]
        try:
            review.find_element_by_partial_link_text("...more").click()
        except NoSuchElementException:
            print("nvm")
            
        list.append(url)    
        list.append(review.text.replace('\n', ' ').replace(',', '').replace('(less)', '').replace("'", ""))
        print(list)
        export(list)
        print("Exported #",i," of ",size)
        i = i + 1  

def export(list):
    filename = pathlib.Path("./data/raw_data.csv")
    f = open(filename, "a+", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(list)
    f.close()

if __name__ == "__main__":
    scrapedata()
    
    
