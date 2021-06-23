# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 01:48:03 2021

@author: Administrator
"""
import pandas as pd
import re
import string
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity

r = Rake() 

def rake():
    df = pd.read_csv('./data/cleaned_data_for_rake.csv', index_col=[0, 1])
        
    df['keywords'] = df['review'].apply(lambda x: rake_implement(x,r))

    print(df.head())
    
    df.to_csv('./data/postrake.csv')


def rake_implement(x,r):
     r.extract_keywords_from_text(x)
     return r.get_ranked_phrases()


def countvectorizer(title):
    df = pd.read_csv('./data/postrake.csv', index_col=[0, 1])
    indices = pd.Series(df['URL'])
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['review'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    print(cosine_sim)
    recommended_books = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indices = list(score_series.iloc[1:11].index)
    
    for i in top_10_indices:
        recommended_books.append(list(df['URL'])[i])
        
    print(recommended_books)


if __name__ == "__main__":
    supervisedl()