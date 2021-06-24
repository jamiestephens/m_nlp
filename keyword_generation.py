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
import csv


r = Rake() 

def rake():
    df = pd.read_csv('keyworded_concatenated.csv', index_col=[0, 1])
        
    df['keywords'] = df['review'].apply(lambda x: rake_implement(x,r))

    print(df.head())
    
    return df


def rake_implement(x,r):
     r.extract_keywords_from_text(x)
     return r.get_ranked_phrases()


if __name__ == "__main__":
 #  rake()