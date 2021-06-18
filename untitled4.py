# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 01:26:13 2021

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

def scrapedata():
    URL = 'https://www.goodreads.com/book'
    driver = webdriver.Firefox(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\geckodriver\geckodriver.exe')
    driver.maximize_window()
    driver.get(URL)
    wait = WebDriverWait(driver, 5)
    time.sleep(3)
    driver.refresh()
    driver.refresh()
    
    ratingarray = ['5 stars','4 stars','3 stars']
    reviewarray = []
    df = pd.DataFrame(columns=['Title', 'Author', 'Link','Description',
                            'Rev5-1','Rev5-2','Rev5-3','Rev5-4','Rev5-5','Rev5-6','Rev5-7',
                            'Rev4-1','Rev4-2','Rev4-3','Rev4-4','Rev4-5','Rev4-6','Rev4-7',
                            'Rev3-1','Rev3-2','Rev3-3','Rev3-4','Rev3-6','Rev3-7'])
    
    searchbar1 = driver.find_element_by_id('explore_search_query')
    
    with open('test.csv', 'r') as read_obj:
        csv_reader = DictReader(read_obj)
        column_names = csv_reader.fieldnames
        for row in csv_reader:
            print(row['search'])
           # try: 
            searchbar1.send_keys(row['search'])
            searchbar1.send_keys(Keys.ENTER)
            time.sleep(5)
            driver.find_element_by_xpath('//a[contains(@href,"book/show")]').click()
            time.sleep(5)
            reviews = driver.find_elements_by_xpath('//div[@class="reviewText stacked"]')
                  
            try:
                morelink = driver.find_element_by_xpath("//*[@id='descriptionContainer']")
                morelink.find_element_by_partial_link_text("...more").click()
            except NoSuchElementException:
                pass
            
            for i in ratingarray:
                try:
                    morefilter = driver.find_element_by_xpath('//div[@id="reviewControls"]')
                    morefilterlink = morefilter.find_element_by_partial_link_text("More filters")
                    morefilterlink.click()
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, r'/html/body/div[7]/div[1]/div/ul/li[2]/div/div/div[2]/div[1]/span[1]/a'))).click()
                    print("yep 2")
                    try:
                        action = ActionChains(driver)
                        ratingclick = driver.find_element_by_xpath('//div[@class="borderCenter"]')
                        ratingsavail = ratingclick.find_element_by_partial_link_text(i).click()
                        print("IT WORKED")
                    except NoSuchElementException:
                        print("oh no")
                except NoSuchElementException:
                    print("oh no")
                    pass
                    
                time.sleep(10)
                i = 0
                
                size = 7
                
                if len(reviews) < 7:
                    size == len(reviews)
            
                print(size)
                
                for i in range(0,7):
                    review = driver.find_elements_by_xpath('//div[@class="reviewText stacked"]')[i]
                    try:
                        revbutton = review.find_element_by_partial_link_text("...more").click()
                    except NoSuchElementException:
                        pass
                    reviewarray.append(review.text.replace('\n', ' ').replace('(less)', '').replace("'", ""))
                    i = i + 1
            
            
            print(reviewarray)
            list = [driver.find_element_by_xpath('//h1[@class="gr-h1 gr-h1--serif"]').text,
                    driver.find_element_by_xpath("//*[@id='description']").text.replace('\n', ' ').replace('(less)',''),
                    driver.current_url]
            
            list.append(reviewarray)

if __name__ == "__main__":
    scrapedata()
    
    

