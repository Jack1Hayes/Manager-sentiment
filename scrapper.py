# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 10:34:10 2022

@author: Hayes

web scrapper
"""

import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import seaborn as sns; sns.set(font_scale=1.2)

# get the response in the form of html
wikiurl, EPLurl="https://en.wikipedia.org/wiki/List_of_Premier_League_managers", "https://www.skysports.com/premier-league-table"
Wikiresponse, response =requests.get(wikiurl), requests.get(EPLurl)

EPLsoup = BeautifulSoup(response.text, 'html.parser')
EPLtable=EPLsoup.find('table',{'class':"standing-table__table"})

# parse data from the html into a beautifulsoup object
soup = BeautifulSoup(Wikiresponse.text, 'html.parser')
managertable=soup.find('table',{'class':"wikitable sortable plainrowheaders"})

dfEPL=pd.read_html(str(EPLtable))
# convert list to dataframe
dfEPL=pd.DataFrame(dfEPL[0])


df=pd.read_html(str(managertable))
# convert list to dataframe
df=pd.DataFrame(df[0])

# organize data
manager_names_table = df.loc[df['Until'] == 'Present*']
manager_names = manager_names_table.drop(["Nat.", "Until", "Ref.", "Years inLeague"], axis=1)
manager_names = manager_names[~manager_names['Name'].astype(str).str.contains('§')]
manager_names = manager_names.replace(to_replace=r'&', value='and', regex=True)
manager_names = manager_names.replace(to_replace=r'ü', value='u', regex=True)
data = df.drop(["Nat.", "Ref."], axis=1)


Final_Table = pd.merge(dfEPL, manager_names, left_on=['Team'], 
             right_on= ['Club'], how='left')
Final_Table = Final_Table.drop("Club", axis=1)


#create twitter handle table

Single_manager_names = manager_names
Single_manager_names.loc[Single_manager_names['Name'].str.split().str.len() >= 2, 'last name'] = Single_manager_names['Name'].str.split().str[-1]
First_Single_manager_names = manager_names
First_Single_manager_names.loc[Single_manager_names['Name'].str.split().str.len() >= 2, 'first name'] = Single_manager_names['Name'].str.split().str[0]

Team_Twitter = pd.DataFrame({'Club': manager_names['Club'],
                'Twiiter name': ['Arsenal', 'AVFCOfficial', 'afcbournemouth', 'Brentfordfc', 'OfficialBHAFC',
                'ChelseaFC', 'CPFC', 'Everton', 'FulhamFC', 'LUFC', 'LCFC', 'LFC', 'ManCity', 
                'ManUtd', 'NUFC', 'NFFC', 'SouthamptonFC', 'SpursOfficial', 'WestHam', 'Wolves']})


Twitter_table = pd.merge(Single_manager_names, Team_Twitter, left_on=['Club'], 
             right_on= ['Club'], how='left')
Twitter_table = pd.merge(First_Single_manager_names, Team_Twitter, left_on=['Club'], 
             right_on= ['Club'], how='left')

#save final tables
Final_Table.to_csv('file path for EPL+Manager_Table.csv' ,mode='w+',  index = False)
Twitter_table.to_csv('file path for TwitterHandle+Manager_names_Table.csv' ,mode='w+',  index = False)
data.to_csv('file path for AllManager_names_Table.csv' ,mode='w+',  index = False)

