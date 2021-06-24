# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:11:58 2021

@author: Administrator
"""

import pandas as pd
import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from nltk.corpus import stopwords
from textdistance import levenshtein
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np 
from nltk.tag import pos_tag
from timeit import default_timer as timer
from nltk.stem.wordnet import WordNetLemmatizer
import csv
import nltk
from textblob import TextBlob

df = pd.read_csv('./data/processed_data_prelim.csv')
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

def wordreplacement():
    global df
    with open('replace_words.csv') as infile:
        reader = csv.reader(infile)
        replace_dict = {rows[0]:rows[1] for rows in reader}
        
    df['review'] = df['review'].replace(replace_dict, regex=True)
    return df

def stopwords():
    global df
    
    return df

def addtlcleaning():  
    global df
        
    v = TfidfVectorizer(max_features=90)
    x = v.fit_transform(df['review'])
    
    print(timer()-start)
    start = timer()
    
    exclusions = ['time','world','first','good']
    mostcommonwords = v.get_feature_names()
    
    for ele in exclusions:
        if ele in mostcommonwords:
            mostcommonwords.remove(ele)
    
    print(timer()-start)
    start = timer()   
    
    df["review"].replace(mostcommonwords, "", inplace=True)
    
    with open('extra_stopwords.csv',newline='') as f:
        reader = csv.reader(f)
        extrastopwords = list(reader)
    
    print(timer()-start)
    start = timer()
    
    stop = stopwords.words('english')
    
    df['review'] = df['review'].apply(lambda x: [item for item in x if item not in stop])
   
    print(timer()-start)
    start = timer()
    
    v1 = TfidfVectorizer(max_df = 1)
    x1 = v1.fit_transform(df['review'])
    one_off_words = v1.get_feature_names()
    
    df["review"].replace(one_off_words, "", inplace=True)
    
    

    
    print(timer()-start)
    start = timer()

    return df

def lemmatizer():
    global df
    

def lemmatization(text):
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

def removelowratings():
    global df
    df.rating.value_counts(normalize=True)
    df = df[df.rating!=0]
    df = df[df.rating!=1]
    df = df[df.rating!=2] 
    df = df[df.rating!=3] 
    df = df.reset_index(drop=True)
    del df['rating']
    return df    

def whitespacesdashslash():
    global df
    df.review= df.review.str.replace('      ',' ',regex=True)    
    df.review= df.review.str.replace('     ',' ',regex=True) 
    df.review= df.review.str.replace('    ',' ',regex=True) 
    df.review= df.review.str.replace('   ',' ',regex=True) 
    df.review= df.review.str.replace('  ',' ',regex=True) 
    df.review= df.review.str.replace('-',' ',regex=True) 
    df.review= df.review.str.replace('/',' ',regex=True) 
    return df

def removesmallreviews():
    global df
    df = df[df['review'].str.len() >= 14]  
    return df

def alphabetizelowercasealphanumeric():
    global df
    alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)   
    punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())
    df['review'] = df.review.map(alphanumeric).map(punc_lower) 
    repeating_chars = lambda x: re.sub(r'([a-z])\1{2,}',r'\1',x)
    df['review'] = df.review.map(repeating_chars)
    #df.apply(lambda x: levenshtein.distance(x['review'],  x['review']), axis=1)
    #df.apply(lambda x: " ".join([TextBlob(i).correct() for i in df['review'].split()]))
    df['review'] = df['review'].apply(lambda x: TextBlob(x).correct())
    removesingleletters = lambda x: re.sub(r'(?i)\b[a-z]\b','',x)
    df['review'] = df.review.map(removesingleletters)
    return df

def removeforeignwords():
    global df
    foreignwordsgetrid = pd.read_csv('getridofentirereview_words.csv')
    for index, row in foreignwordsgetrid.iterrows():
        df[~df.review.str.contains(row['foreignword'])]
    return df

def tokenization():
    global df
    pass

def concatenated():
    # takes a dataframe with 1 review per row; returns one distinct book per row with all
    # review/keyword text concatenated
    global df
    df = df.groupby('URL')
    df = df['review'].agg(lambda column: " ".join(column))
    df = df.reset_index(name="review")
    return df

def arraytolist():
    global df
    df['review'] = [','.join(map(str, l)) for l in df['review']]
    return df

def main():
    start = timer()
    removelowratings()
    whitespacesdashslash()
    alphabetizelowercasealphanumeric()
    removeforeignwords()
    whitespacesdashslash()
    removesmallreviews()
    tokenization()
   # addtlcleaning()
   # concatenated()
   # print(df.head())
    df.to_csv('./data/cleaneddata.csv')
    print("Total time: ",timer()-start)
    
main()
