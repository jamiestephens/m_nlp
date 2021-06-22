# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:11:58 2021

@author: Administrator
"""

import pandas as pd
import re
import string
import nltk

def cleaningthefile():
    df = pd.read_csv('./data/rawdata.csv', names=['URL', 'review2','review3','review4','review5'], header=None,low_memory=False)
    print(len(pd.unique(df['URL'])))
    df['review2'] = df['review2'].replace({';':''}, regex=True)
    df['review3'] = df['review3'].replace({';':''}, regex=True)
    df['review4'] = df['review4'].replace({';':''}, regex=True)
    df['review5'] = df['review5'].replace({';':''}, regex=True)
    df['review'] = df['review2'].astype(str) + df['review3'].astype(str) + df['review4'].astype(str) + df['review5'].astype(str) 
    del df['review2']
    del df['review3']
    del df['review4']
    del df['review5']
    df['review'] = df['review'].str.split(' flag').str[0]
    df.review= df.review.str.replace(' rated it it was amazing',' Rating 5/5-',regex=True)    
    df.review= df.review.str.replace(' rated it really liked it',' Rating 4/5-',regex=True)    
    df.review= df.review.str.replace(' rated it liked it',' Rating 3/5-',regex=True)    
    df.review= df.review.str.replace(' rated it it was ok',' Rating 2/5-',regex=True)    
    df.review= df.review.str.replace(' rated it did not like it',' Rating 1/5-',regex=True)    
    df.review= df.review.str.replace(' marked it as dnf ',' Rating 0/5-',regex=True)        
    df.review= df.review.str.replace(' ·  review of another edition',' ',regex=True)    
    df.review= df.review.str.replace(' · review of another edition',' ',regex=True)    
    df[~df.review.str.contains(" added it")]
    df[~df.review.str.contains(" marked it as return-to-later ")]
    df[~df.review.str.contains(" marked it as to-read ")]
    df[~df.review.str.contains(" is currently reading it ")]
    df[~df.review.str.contains(" marked it as started-but-didn-t-finish ")]
    df[~df.review.str.contains(" marked it as on-hold ")]
    df[~df.review.str.contains(" marked it as to-read-own ")]
    
    df.review= df.review.str.replace('Shelves:',' ',regex=True) 
    df[df.review == 'Rating']
    df['rating'] = df['review'].str.split('/5-').str[0]
    df['rating'] = df['rating'].str.split('g ').str[-1]    
    df['review'] = df['review'].str.split('/5-').str[-1]
    df.to_csv('./data/processed_data_prelim.csv')


def addtlcleaning():
    df = pd.read_csv('./data/processed_data.csv')
    print(df.head())
    print(len(pd.unique(df['URL'])))
    
    alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
    df.review= df.review.str.replace('This review has been hidden because it contains spoilers. To view it click here.','',regex=True)    
    df.review= df.review.str.replace('(view spoiler)','',regex=True)    
    punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())
    df['review'] = df.review.map(alphanumeric).map(punc_lower) 
    
    words = set(nltk.corpus.words.words())
    
    text_translated = df.text.apply(words)
    
    df.to_csv('./data/processed_data_final.csv')

def edafile():
    df1=pd.read_csv('./data/output_ratings_rev.csv')
    print(df1.head())
    
    print(len(pd.unique(df1['URL'])))

if __name__ == "__main__":
    addtlcleaning()