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
def supervisedl():
    df = pd.read_csv('./data/output_ratings_rev.csv')
    df.rating.value_counts(normalize=True)
    df = df[df.rating!=0]
    df = df[df.rating!=1]
    df = df[df.rating!=2]    
    
    df['sentiment'] = np.where(df['rating'] >= 4, 'positive', 'negative')
    
    print(df.head())
    
    X = df.review
    y = df.sentiment
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    tfidf1 = TfidfVectorizer(stop_words='english')
    X_train_tfidf1 = tfidf1.fit_transform(X_train)
    X_test_tfidf1  = tfidf1.transform(X_test)

    tfidf2 = TfidfVectorizer(ngram_range=(1,2), binary=True, stop_words='english')
    X_train_tfidf2 = tfidf2.fit_transform(X_train)
    X_test_tfidf2  = tfidf2.transform(X_test)

  #  lr.fit(X_train_tfidf1, y_train)
  #  y_pred_tfidf1_lr = lr.predict(X_test_tfidf1)
  #  cm5 = conf_matrix(y_test, y_pred_tfidf1_lr)

def rake():
    df = pd.read_csv('test1.csv')
        
    df.rating.value_counts(normalize=True)
    df = df[df.rating!=0]
    df = df[df.rating!=1]
    df = df[df.rating!=2]    
    
    del df['rating']
    
    grouped_df = df.groupby('URL')
    
    grouped_lists = grouped_df['review'].agg(lambda column: " ".join(column))
    
    grouped_lists = grouped_lists.reset_index(name="review")

    grouped_lists['keywords'] = grouped_lists['review'].apply(lambda x: rake_implement(x,r))

    print(grouped_lists.head())
    
    grouped_lists.to_csv('outputwithkeywords1.csv')


def rake_implement(x,r):
     r.extract_keywords_from_text(x)
     return r.get_ranked_phrases()


def countvectorizer(title):
    df = pd.read_csv('outputwithkeywords1.csv')
    indices = pd.Series(df['URL'])
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['keywords'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    print(cosine_sim)
    recommended_books = []
    idx = indices[indices == URL].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indices = list(score_series.iloc[1:11].index)
    
    for i in top_10_indices:
        recommended_books.append(list(df['Title'])[i])
    return recommended_books

if __name__ == "__main__":
    countvectorizer()