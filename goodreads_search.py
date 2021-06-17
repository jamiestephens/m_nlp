# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 21:58:31 2021

@author: Jamie Stephens
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import action_chains
import time
from csv import reader

def csvopen(file):   
    URL = 'https://www.goodreads.com/book/show/350.Stranger_in_a_Strange_Land'
    driver = webdriver.Firefox(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\geckodriver\geckodriver.exe')
    driver.maximize_window()
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    print("yes")
    time.sleep(15)
    driver.refresh()
    driver.refresh()
    with open(file, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            print(row[0])
            getbookinfo(row[0])

def getbook():
    URL = 'https://www.goodreads.com/book/show/350.Stranger_in_a_Strange_Land'
    driver = webdriver.Firefox(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\geckodriver\geckodriver.exe')
    driver.maximize_window()
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    print("yes")
    time.sleep(15)
    driver.refresh()
    driver.refresh()

def getbookinfo(book):
    driver.get(link)

if __name__ == "__main__":
   # getbook()
  # csvopen('wikipediabooks.csv')
    getbookinfo()
    