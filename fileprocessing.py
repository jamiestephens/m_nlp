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
    
    df.rating.value_counts(normalize=True)
   # df = df[df.rating!=0]
   # df = df[df.rating!=1]
   # df = df[df.rating!=2]  
    
    print(df.head())
    print(len(pd.unique(df['URL'])))
    df.review= df.review.str.replace('Like   see reviewnannannan',' ',regex=True)    
    df.review= df.review.str.replace('like   see reviewnannannan',' ',regex=True)
    df.review= df.review.str.replace('ya','young adult',regex=True)    
    alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
    df.review= df.review.str.replace('This review has been hidden because it contains spoilers. To view it click here.','',regex=True)      
    df.review= df.review.str.replace('dnfing','dnf',regex=True)    
    df.review= df.review.str.replace('time-travel','time travel',regex=True)  
    df.review= df.review.str.replace('dystopic','dystopia',regex=True)  
    df.review= df.review.str.replace('dystopian','dystopia',regex=True) 


    
    df.apply(lambda x: levenshtein.distance(x['review'],  x['review']), axis=1)
   
    
    df.review= df.review.str.replace('young adult','youngadult',regex=True)    
    punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())
    df['review'] = df.review.map(alphanumeric).map(punc_lower) 
    
    df.review= df.review.str.replace(' havent ',' ',regex=True)
    df.review= df.review.str.replace(' dont ',' ',regex=True)
    df.review= df.review.str.replace(' http ',' ',regex=True)
    df.review= df.review.str.replace(' didnt ',' ',regex=True)
    df.review= df.review.str.replace(' www ',' ',regex=True)
    df.review= df.review.str.replace(' youtube ',' ',regex=True)
    df.review= df.review.str.replace(' com ',' ',regex=True)
    df.review= df.review.str.replace(' e ',' ',regex=True)
    df.review= df.review.str.replace(' book ',' ',regex=True)   
    df.review= df.review.str.replace(' wa ',' ',regex=True)   
    df.review= df.review.str.replace(' arc ',' ',regex=True)    
    df.review= df.review.str.replace(' (view spoiler) ',' ',regex=True)    
    df.review= df.review.str.replace(' childrens ',' children ',regex=True)  
    df.review= df.review.str.replace(' likenannannan ',' ',regex=True)
    df.review= df.review.str.replace(' literature ','',regex=True)
    df.review= df.review.str.replace(' reread ','',regex=True)
    df.review= df.review.str.replace(' rereading ','',regex=True)
    df.review= df.review.str.replace(' abridged ',' ',regex=True)
    df.review= df.review.str.replace(' unabridged ',' ',regex=True)
    df.review= df.review.str.replace(' movie ',' ',regex=True)
    df.review= df.review.str.replace(' adapted ',' ',regex=True)
    df.review= df.review.str.replace(' adaptation ',' ',regex=True)
    df.review= df.review.str.replace(' sci-fi ',' ',regex=True)
    df.review= df.review.str.replace(' scifi ',' ',regex=True)
    df.review= df.review.str.replace(' sci ',' ',regex=True)
    df.review= df.review.str.replace(' fi ',' ',regex=True)
    df.review= df.review.str.replace(' sf ',' ',regex=True)
    df.review= df.review.str.replace(' science fiction ',' ',regex=True)
    df.review= df.review.str.replace(' science ',' ',regex=True)
    df.review= df.review.str.replace(' spoiler',' ',regex=True)
    df.review= df.review.str.replace(' fiction',' ',regex=True)
    df.review= df.review.str.replace(' cover',' ',regex=True)
    df.review= df.review.str.replace(' im ',' ',regex=True)
    df.review= df.review.str.replace(' review ',' ',regex=True)
    df.review= df.review.str.replace(' hugo ',' ',regex=True)
    df.review= df.review.str.replace(' movie ',' ',regex=True)
    df.review= df.review.str.replace(' ebook ',' ',regex=True)
    df.review= df.review.str.replace(' e-book ',' ',regex=True)
    df.review= df.review.str.replace(' kindle ',' ',regex=True)
    df.review= df.review.str.replace(' sale ',' ',regex=True)
    df.review= df.review.str.replace(' recommended ',' ',regex=True)
    df.review= df.review.str.replace(' freebie ',' ',regex=True)
    df.review= df.review.str.replace(' recommend ',' ',regex=True)
    df.review= df.review.str.replace(' recommended ',' ',regex=True)
    df.review= df.review.str.replace(' novel ',' ',regex=True)
   
    df.review= df.review.str.replace(' really ',' ',regex=True)
    df.review= df.review.str.replace(' shelves ',' ',regex=True) 
    df.review= df.review.str.replace(' read ',' ',regex=True)        
    df.review= df.review.str.replace(' reading ',' ',regex=True)    
    df.review= df.review.str.replace(' audio ',' ',regex=True)    
    df.review= df.review.str.replace(' audiobook ',' ',regex=True)    
    df.review= df.review.str.replace(' audiobooks ',' ',regex=True)    
    df.review= df.review.str.replace(' author ',' ',regex=True)    
    df.review= df.review.str.replace(' novel ',' ',regex=True)    
    df.review= df.review.str.replace(' chapter ',' ',regex=True)   
    df.review= df.review.str.replace(' nominee ',' ',regex=True)   
    df.review= df.review.str.replace(' nebula ',' ',regex=True)   
    df.review= df.review.str.replace(' story ',' ',regex=True)   
    df.review= df.review.str.replace(' finalist ',' ',regex=True)  
    df.review= df.review.str.replace(' recommendation ',' ',regex=True)   
    df.review= df.review.str.replace(' ive ',' ',regex=True)        
    df.review= df.review.str.replace(' page ',' ',regex=True)
    df.review= df.review.str.replace(' pages',' ',regex=True)    
    df.review= df.review.str.replace(' sample',' ',regex=True)       
    df.review= df.review.str.replace(' used',' ',regex=True)    
    df.review= df.review.str.replace(' copy',' ',regex=True)    
    df.review= df.review.str.replace(' writer',' ',regex=True)    
    df.review= df.review.str.replace(' novelist ',' ',regex=True)    
    df.review= df.review.str.replace(' goodreads ',' ',regex=True)    
    df.review= df.review.str.replace(' goodread ',' ',regex=True)    
    df.review= df.review.str.replace(' shelf ',' ',regex=True)    
    df.review= df.review.str.replace(' shelves ',' ',regex=True)    
    df.review= df.review.str.replace(' star ',' ',regex=True)    
    df.review= df.review.str.replace(' one ',' ',regex=True)    
    df.review= df.review.str.replace(' two ',' ',regex=True)    
    df.review= df.review.str.replace(' three ',' ',regex=True)    
    df.review= df.review.str.replace(' four ',' ',regex=True)    
    df.review= df.review.str.replace(' five ',' ',regex=True)    
    df.review= df.review.str.replace(' recs ',' ',regex=True)    
    df.review= df.review.str.replace(' favorite ',' ',regex=True)    
    df.review= df.review.str.replace(' wont ',' ',regex=True)    
    df.review= df.review.str.replace(' rate ',' ',regex=True)    
    df.review= df.review.str.replace(' rated ',' ',regex=True)  
    df.review= df.review.str.replace(' fav ',' ',regex=True)  
    df.review= df.review.str.replace(' bookstore ',' ',regex=True)  
    df.review= df.review.str.replace(' bought ',' ',regex=True)
    df.review= df.review.str.replace(' dnfed ',' dnf ',regex=True)
    df.review= df.review.str.replace(' rating ',' ',regex=True)
    df.review= df.review.str.replace(' liked ',' ',regex=True)
    df.review= df.review.str.replace(' originally ',' ',regex=True)
    df.review= df.review.str.replace(' published ',' ',regex=True)
    df.review= df.review.str.replace(' posted ',' ',regex=True)
    df.review= df.review.str.replace(' reviewed ',' ',regex=True)
    df.review= df.review.str.replace(' utopian ',' utopia ',regex=True)
    df.review= df.review.str.replace(' finished ',' ',regex=True)
    df.review= df.review.str.replace(' finish ',' ',regex=True)
    #words = set(nltk.corpus.words.words())
    
    #text_translated = df.text.apply(words)
    df = df.reset_index(drop=True)
    
    df['review'] = df.review.apply(lemmatization)
    stop = stopwords.words('english')
   # stop.extend(new_stopwords)
    
    df['review'] = df['review'].apply(lambda x: [item for item in x if item not in stop])
    
    
    df[df['review'].apply(lambda x: len(x) > 10)]
    df.to_csv('./data/processed_data_semifinal_ratings0-55.csv')

def lemmatization(text):
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

def concatenated():
    df = pd.read_csv('./data/processed_data_final.csv')
    
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
    
    grouped_lists.to_csv('./data/concatenatedreviews_noratings.csv')




def edafile():
    df1=pd.read_csv('./data/output_ratings_rev.csv')
    print(df1.head())
    
    print(len(pd.unique(df1['URL'])))

if __name__ == "__main__":
    addtlcleaning()