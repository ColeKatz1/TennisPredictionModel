from dataclasses import replace
import string
from tokenize import String
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from selenium import webdriver

with open("C:/Users/colek/OneDrive/Desktop/ATP_Serve_Return_Stats/ATP_Serve_4_7_22.html") as fp:
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


with open("C:/Users/colek/OneDrive/Desktop/ATP_Serve_Return_Stats/ATP_Return_4_7_22.html") as fp:
    soupReturn = BeautifulSoup(fp, 'html.parser')

trReturn = soupReturn.findAll('tr', class_ = "stats-listing-row")

return_data = [[td.getText() for td in trReturn[i].findAll(['th','td'])]
        for i in range(len(trReturn))
        ]

dfReturn = pd.DataFrame(return_data)
dfReturn = dfReturn.drop(0,axis=1)

dfReturn.columns = ['Player', 'Return_Rating','1st_Serve_Return_Pct', '2nd_Serve_Return_Pct','Return_Games_Won_Pct','Break_Points_Won_Pct']


firstServeReturnPct = dfReturn['1st_Serve_Return_Pct'].astype(str)
firstServeReturnPct = firstServeReturnPct.tolist()
firstServeReturnPct = [i.replace('%','') for i in firstServeReturnPct]

secondServeReturnPct = dfReturn['2nd_Serve_Return_Pct'].astype(str)
secondServeReturnPct = secondServeReturnPct.tolist()
secondServeReturnPct = [i.replace('%','') for i in secondServeReturnPct]


dfReturn['1st_Serve_Return_Pct'] = firstServeReturnPct
dfReturn['2nd_Serve_Return_Pct'] = secondServeReturnPct

dfReturn['1st_Serve_Return_Pct'] = pd.to_numeric(dfReturn['1st_Serve_Return_Pct'])
dfReturn['2nd_Serve_Return_Pct'] = pd.to_numeric(dfReturn['2nd_Serve_Return_Pct'])


#.651(70-19.8)+.349(53.1-39.7) + 50 to find their chances of winning on serve, this is a great formula. takes into account how often they make the first serve

def calculateServePct(playerName1, playerName2):
    player1Serve = data.loc[data['Player'] == playerName1]
    player2Serve = data.loc[data['Player'] == playerName2]
    player1Return = dfReturn.loc[dfReturn['Player'] == playerName1]
    player2Return = dfReturn.loc[dfReturn['Player'] == playerName2]
    player1FirstServeProp = player1Serve['1st_Serve_Pct'] / 100
    player2FirstServeProp = player2Serve['1st_Serve_Pct'] / 100
    player1SecondServeProp = player1Serve['2nd_Serve_Pct'] / 100
    player2SecondServeProp = player2Serve['2nd_Serve_Pct'] / 100
    player1FirstServeWon = player1Serve['1st_Serve_Won_Pct'] 
    player2FirstServeWon = player2Serve['1st_Serve_Won_Pct'] 
    player1SecondServeWon = player1Serve['2nd_Serve_Won_Pct'] 
    player2SecondServeWon = player2Serve['2nd_Serve_Won_Pct'] 
    player1FirstServeReturnPct = player1Return['1st_Serve_Return_Pct']
    player2FirstServeReturnPct = player2Return['1st_Serve_Return_Pct']
    player1SecondServeReturnPct = player1Return['2nd_Serve_Return_Pct']
    player2SecondServeReturnPct = player2Return['2nd_Serve_Return_Pct']
    #p1 = player1FirstServeProp.values
    p1 = player1FirstServeProp.values*(player1FirstServeWon.values-(player2FirstServeReturnPct.values)) + player1SecondServeProp.values*(player1SecondServeWon.values-(player2SecondServeReturnPct.values)) + 40
    p2 = player2FirstServeProp.values*(player2FirstServeWon.values-player1FirstServeReturnPct.values) + player2SecondServeProp.values*(player2SecondServeWon.values-player1SecondServeReturnPct.values) + 40

    #print(playerName1, p1) 
    #print(playerName2, p2)
    return(p1,p2)
    #print(player1SecondServeProp)

#calculateServePct("Jaume Munar", "Tallon Griekspoor") 



#eloDF = pd.read_csv("C:/Users/colek/OneDrive/Desktop/Tennis_Prediction_Model/Elo_Ratings.csv")

#eloDF = eloDF.dropna(axis=1)
#eloDF = eloDF[['Player','Elo']]
#df = pd.merge(dfReturn, data, on='Player')

#eloDF['Player'] = eloDF['Player'].astype(str)
#eloDF['Elo'] = eloDF['Elo'].astype(int)
#df['Player'] = df['Player'].astype(str)

#df = pd.merge(df, eloDF, on='Player')

#print(df)
#print(eloDF)
