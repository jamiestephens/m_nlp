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
import pickle
import numpy as np 

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

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
    df = pd.read_csv('./data/processed_data_prelim.csv')
    
    df = df[df.rating!=0]
    df = df[df.rating!=1]
    df = df[df.rating!=2]  
    
    df.review= df.review.str.replace('      ',' ',regex=True)    
    df.review= df.review.str.replace('     ',' ',regex=True) 
    df.review= df.review.str.replace('    ',' ',regex=True) 
    df.review= df.review.str.replace('   ',' ',regex=True) 
    df.review= df.review.str.replace('  ',' ',regex=True) 
    df = df[df['review'].str.len() >= 10]  
    
    print(df.head())
    print(len(pd.unique(df['URL'])))
    df.review= df.review.str.replace('Like   see reviewnannannan',' ',regex=True)    
    df.review= df.review.str.replace('like   see reviewnannannan',' ',regex=True)
    df.review= df.review.str.replace('worldcrafting','worldbuild',regex=True)
    df.review= df.review.str.replace('worldbuilding','worldbuild',regex=True)
    df.review= df.review.str.replace('world building','worldbuild',regex=True)
    df.review= df.review.str.replace('world-building','worldbuild',regex=True)
    
    
    df.review= df.review.str.replace('Recommends it for ',' ',regex=True)
    df.review= df.review.str.replace('ya','young adult',regex=True)    
    alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
    df.review= df.review.str.replace('This review has been hidden because it contains spoilers. To view it click here.','',regex=True)      
    df.review= df.review.str.replace('dnfing','dnf',regex=True)    
    df.review= df.review.str.replace('time-travel','time travel',regex=True)  
    df.review= df.review.str.replace('dystopic','dystopia',regex=True)  
    df.review= df.review.str.replace('dystopian','dystopia',regex=True) 
    df.review= df.review.str.replace('dystopians','dystopia',regex=True)     
 
    df.apply(lambda x: levenshtein.distance(x['review'],  x['review']), axis=1)
   
    
    df.review= df.review.str.replace('youngadult','young adult',regex=True)    
    punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())
    df['review'] = df.review.map(alphanumeric).map(punc_lower) 
    
    df.review= df.review.str.replace('ha','',regex=True)

    
    getrid = pd.read_csv('getrid.csv')
    for index, row in getrid.iterrows():
        phrase = " " + row['getridofit'] + " "
        df.review= df.review.str.replace(phrase,' ',regex=True)
   
    df.review= df.review.str.replace(' childrens ',' children ',regex=True)   
    
    foreignwordsgetrid = pd.read_csv('foreigngetrid.csv')
    for index, row in foreignwordsgetrid.iterrows():
        phrase1 = " " + row['foreignword'] + " "
        df.review= df.review.str.replace(phrase1,' ',regex=True)
     
    df = df.reset_index(drop=True)
    
    v = TfidfVectorizer(max_features=80)
    x = v.fit_transform(df['review'])
    print(v.get_feature_names())
    
    mostcommonwords = v.get_feature_names()
    mostcommonwords.remove('time')
    mostcommonwords.remove('world')
    mostcommonwords.remove('first')
    mostcommonwords.remove('good')
    df["review"].replace(mostcommonwords, "", inplace=True)
    
    v1 = TfidfVectorizer(max_df = 1)
    x1 = v1.fit_transform(df['review'])
    leastcommonwords = v1.get_feature_names()
    print(type(leastcommonwords))
    
    np.savetxt("leastcommonwordssub1.csv", 
           leastcommonwords,
           delimiter =", ", 
           fmt ='% s')
        
    df.to_csv('./data/cleaned_data_for_rake.csv')

    df['review'] = df.review.apply(lemmatization)
    
    stop = stopwords.words('english')
    
    df['review'] = df['review'].apply(lambda x: [item for item in x if item not in stop])
    

    df.to_csv('./data/processed_data_final1.csv')

def lemmatization(text):
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

def concatenated():
    df = pd.read_csv('./data/processed_data_prelim.csv')
    
    print(df.head())
    
    df.rating.value_counts(normalize=True)
    df = df[df.rating!=0]
    df = df[df.rating!=1]
    df = df[df.rating!=2]    
    
    del df['rating']
    
    grouped_df = df.groupby('URL')
    
    grouped_lists = grouped_df['review'].agg(lambda column: " ".join(column))
    
    grouped_lists = grouped_lists.reset_index(name="review")

    print(grouped_lists.head())
    
    grouped_lists.to_csv('./data/concatenatedreviews_new.csv')


def concatenated_after_keywording():
    df = pd.read_csv('./data/postrake.csv', index_col=[0, 1])
   
    df = df.groupby('URL')
    
    df = df['keywords'].agg(lambda column: " ".join(column))
    
    print(df.head())
    
    df = df.reset_index(name="keywords")
    
    df.to_csv('./data/keyworded_concatenated.csv')


def edafile():
    df1=pd.read_csv('./data/output_ratings_rev.csv')
    print(df1.head())
    
    print(len(pd.unique(df1['URL'])))

if __name__ == "__main__":
    addtlcleaning()