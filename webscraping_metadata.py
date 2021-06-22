# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 01:58:42 2021

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
    
    with open('URLs.csv', 'r') as read_obj:
        csv_reader = DictReader(read_obj)
        column_names = csv_reader.fieldnames
        i = 1
        j = 7
        for row in csv_reader:
            print("{}: {}".format(i,row['search']))
            list = []
            URL = row['search']
            driver.get(URL)
            time.sleep(5)
            try:
                print("Yes 1/5")
          #     try:
                morelink = driver.find_element_by_xpath("//*[@id='descriptionContainer']")
                morelink.find_element_by_partial_link_text("...more").click()
            except NoSuchElementException:
                print("Nvm 1/2")
            
            try:
                description = driver.find_element_by_xpath("//*[@id='description']").text.replace('\n', ' ').replace(',', '').replace('(less)','')
            except NoSuchElementException:
                description = ""
            
            print("Yes 2/5")
            list = [driver.find_element_by_xpath('//h1[@class="gr-h1 gr-h1--serif"]').text,
                    driver.find_element_by_xpath("//*[@id='bookAuthors']").text,
                    driver.current_url,
                    description]
            print("Yes 3/5")
            
            try:
                driver.find_element_by_partial_link_text("next »").click()
                time.sleep(5)
                revarrayparttwo = copyreviews(driver)
                print("Yes 4/5")
            except NoSuchElementException:
                print("Nvm 2/2")
            
            print("Yes 5/5")
            list = list + revarray
            
            if i % 10 == 0:
                 j += 1
            
            export(list,j)
         #   except:
               # print("^ Couldn't locate this one")

            driver.get(URL)  
            i += 1

def export(list,j):
    filename = pathlib.Path("./data/metadata.csv")
    if filename.exists():
        f = open(filename, "a+", encoding="utf-8")
        writer = csv.writer(f)
        writer.writerow(list)
        print("Exported")
        f.close()
    else:
        with open(filename, 'w') as fp:
            print("New file")
        fp.close()
        export(list,j)

if __name__ == "__main__":
    scrapedata()
    
    

