# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 11:11:54 2022

@author: Hayes

tweet analysis
"""

import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import seaborn as sns; sns.set(font_scale=1.2)
from textblob import TextBlob
from datetime import datetime, timedelta


Twitter_table = pd.read_csv('file where TwitterHandle+Manager_names_Table.csv is located')  
    
def sentiment_scores(text_data):

        # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
   # Text_sid_obj = TextBlob(df).sentiment.subjectivity
    #Text_pol_obj = TextBlob(df).sentiment.polarity

    neg_score_vad=[]
    neu_score_vad=[]
    pos_score_vad=[]
    score_textblob = []
    pol_textblob = []
        
    for tweets in df:
        sentiment_dict = sid_obj.polarity_scores(tweets)
        Text_sid_obj = TextBlob(tweets).sentiment.subjectivity
        Text_pol_obj = TextBlob(tweets).sentiment.polarity
        
        neg_score_vad.append(sentiment_dict['neg']*100)
        neu_score_vad.append(sentiment_dict['neu']*100)
        pos_score_vad.append(sentiment_dict['pos']*100)
        score_textblob.append(Text_sid_obj)
        pol_textblob.append(Text_pol_obj)
        
        
    text_data['neg score'] = neg_score_vad
    text_data['neu score'] = neu_score_vad
    text_data['pos score'] = pos_score_vad
    text_data['textblob'] = score_textblob
    text_data['textblob_pol'] = pol_textblob
    
    return

negarray = []
neuarray = []
posarray = []
time = (datetime.now()-timedelta(days=21))

for i in Twitter_table.index:
    try:
        anal_data = pd.read_csv('file path for Twitter table'+str(Twitter_table['Club'][i][:3])+str(Twitter_table['Club'][i][-1])+'.csv')
        if datetime.strptime(anal_data['created_at'][i][:19], '%Y-%m-%d %H:%M:%S') > time:
            df = anal_data['text']
            text_data = pd.DataFrame(df, columns = ['text'])
            
                
            sentiment_scores(text_data)
            
            ave_neg = np.average(text_data['neg score'])
            negarray.append(ave_neg)
            ave_neu = np.average(text_data['neu score'])
            neuarray.append(ave_neu)
            ave_pos = np.average(text_data['pos score'])
            posarray.append(ave_pos)
            #ave_text = np.average(text_data['textblob'])
            #ave_text_pol = np.average(text_data['textblob_pol'])
            #print(str(Twitter_table['Club'][i][:3])+'_',ave_neg, ave_neu, ave_pos)#, ave_text, ave_text_pol)
    except:
                
                
            negarray.append(0)
            neuarray.append(0)
            posarray.append(0)
                
scores_data = {'Team': Twitter_table['Club'],
                'negative score': negarray,
                'neutral score': neuarray,
                'positive score': posarray}
scores_table = pd.DataFrame(scores_data)
print(scores_table)
Final_Table = pd.read_csv('file path for EPL+Manager_Table.csv')
Final_Table_Data = pd.merge(scores_table, Final_Table, left_on=['Team'], 
             right_on= ['Team'], how='left')

Final_Table_Data.to_csv('file path and name of sentiment data.csv' , index = False)
