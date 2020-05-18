# -*- coding: utf-8 -*-
"""
Created on Mon May 18 12:10:22 2020

@author: AGrze
"""

import re
import pandas as pd


df= pd.read_csv('18-05jobsInfo.csv', index_col=0)
df = df.astype({'crawl_date':'datetime64'})
df['data_date'] = df['crawl_date']-pd.to_timedelta(df['adsAge']-1, unit='d')
df['data_date'] = df['data_date'].dt.normalize()
df.set_index('data_date', inplace=True)
df = df.sort_index()


def dtd_change(df):
    for column in df:
        if not re.search('company.+|crawl.+|adsAge', column):
            df[column+'_lastday']=df[column].shift(1)
            df['dtd_'+column] = df[column+'_lastday']-df[column]
            

dtd_change(df)
df.to_csv('18-05jobsProcessed.csv')