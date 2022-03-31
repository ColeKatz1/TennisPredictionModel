from dataclasses import replace
import string
from tokenize import String
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from selenium import webdriver

with open("C:/Users/colek/OneDrive/Desktop/Tennis_Prediction_Model/ATP.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

tr = soup.findAll('tr', class_ = "stats-listing-row")

game_data = [[td.getText() for td in tr[i].findAll(['th','td'])]
        for i in range(len(tr))
        ]

data = pd.DataFrame(game_data)
data = data.drop(0,axis=1)
data.columns = ['Player', 'Serve_Rating','1st_Serve_Pct', '1st_Serve_Won_Pct','2nd_Serve_Won_Pct','Serve_Games_Won_Pct','Avg_Aces','Avg_DF']
#print(data)
firstServePct = data['1st_Serve_Pct'].astype(str)
firstServePct = firstServePct.tolist()
firstServePct = [i.replace('%','') for i in firstServePct]

firstServeWonPct = data['1st_Serve_Won_Pct'].astype(str)
firstServeWonPct = firstServeWonPct.tolist()
firstServeWonPct = [i.replace('%','') for i in firstServeWonPct]

secondServeWonPct = data['2nd_Serve_Won_Pct'].astype(str)
secondServeWonPct = secondServeWonPct.tolist()
secondServeWonPct = [i.replace('%','') for i in secondServeWonPct]



#secondServePct = [100 - i for i in firstServePctInt]


data['1st_Serve_Pct'] = firstServePct
data['1st_Serve_Won_Pct'] = firstServeWonPct
data['2nd_Serve_Won_Pct'] = secondServeWonPct

data['1st_Serve_Pct'] = pd.to_numeric(data['1st_Serve_Pct'])
data['1st_Serve_Won_Pct'] = pd.to_numeric(data['1st_Serve_Won_Pct'])
data['2nd_Serve_Won_Pct'] = pd.to_numeric(data['2nd_Serve_Won_Pct'])
data['2nd_Serve_Pct'] = 100 - data['1st_Serve_Pct']
data['Pct_Won_On_Serve'] = (data['1st_Serve_Pct'] / 100 * data['1st_Serve_Won_Pct']) + (data['2nd_Serve_Pct'] / 100 * data['2nd_Serve_Won_Pct'])


with open("C:/Users/colek/OneDrive/Desktop/Tennis_Prediction_Model/Return_ATP.html") as fp:
    soupReturn = BeautifulSoup(fp, 'html.parser')

trReturn = soupReturn.findAll('tr', class_ = "stats-listing-row")

return_data = [[td.getText() for td in trReturn[i].findAll(['th','td'])]
        for i in range(len(trReturn))
        ]

dfReturn = pd.DataFrame(return_data)
dfReturn = dfReturn.drop(0,axis=1)

print(dfReturn)
