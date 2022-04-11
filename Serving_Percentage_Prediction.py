from dataclasses import replace
import string
from tokenize import String
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from selenium import webdriver

with open("C:/Users/colek/OneDrive/Desktop/ATP_Serve_Return_Stats/ATP_Serve_4_7_22.html") as fp: #open html file of serving data
    soup = BeautifulSoup(fp, 'html.parser')

tr = soup.findAll('tr', class_ = "stats-listing-row") #find table of stats

game_data = [[td.getText() for td in tr[i].findAll(['th','td'])] #retrieves the stats from each column in table
        for i in range(len(tr))
        ]

data = pd.DataFrame(game_data) #transforms data into dataframe
data = data.drop(0,axis=1) #drops unneccesary column
data.columns = ['Player', 'Serve_Rating','1st_Serve_Pct', '1st_Serve_Won_Pct','2nd_Serve_Won_Pct','Serve_Games_Won_Pct','Avg_Aces','Avg_DF'] #creates header for columns in dataframe
firstServePct = data['1st_Serve_Pct'].astype(str) 
firstServePct = firstServePct.tolist()
firstServePct = [i.replace('%','') for i in firstServePct] #removes % from the data values in the column

firstServeWonPct = data['1st_Serve_Won_Pct'].astype(str)
firstServeWonPct = firstServeWonPct.tolist()
firstServeWonPct = [i.replace('%','') for i in firstServeWonPct] #removes % from the data values in the column

secondServeWonPct = data['2nd_Serve_Won_Pct'].astype(str)
secondServeWonPct = secondServeWonPct.tolist()
secondServeWonPct = [i.replace('%','') for i in secondServeWonPct] #removes % from the data values in the column



#secondServePct = [100 - i for i in firstServePctInt]


data['1st_Serve_Pct'] = firstServePct #adds back data without % so the numbers can be used
data['1st_Serve_Won_Pct'] = firstServeWonPct #adds back data without % so the numbers can be used
data['2nd_Serve_Won_Pct'] = secondServeWonPct #adds back data without % so the numbers can be used

data['1st_Serve_Pct'] = pd.to_numeric(data['1st_Serve_Pct']) #converts to numeric
data['1st_Serve_Won_Pct'] = pd.to_numeric(data['1st_Serve_Won_Pct']) #converts to numeric
data['2nd_Serve_Won_Pct'] = pd.to_numeric(data['2nd_Serve_Won_Pct']) #converts to numeric
data['2nd_Serve_Pct'] = 100 - data['1st_Serve_Pct'] #creates variable for percent of time second served is used, which is inversely proportional to times when first serve is successful
data['Pct_Won_On_Serve'] = (data['1st_Serve_Pct'] / 100 * data['1st_Serve_Won_Pct']) + (data['2nd_Serve_Pct'] / 100 * data['2nd_Serve_Won_Pct']) #gives percent of points won on a player's serve


with open("C:/Users/colek/OneDrive/Desktop/ATP_Serve_Return_Stats/ATP_Return_4_7_22.html") as fp: #imports returning data, hmtl file downloaded from ATP website
    soupReturn = BeautifulSoup(fp, 'html.parser')

trReturn = soupReturn.findAll('tr', class_ = "stats-listing-row") #finds table in html

return_data = [[td.getText() for td in trReturn[i].findAll(['th','td'])] #goes through each row to extract data from table
        for i in range(len(trReturn))
        ]

dfReturn = pd.DataFrame(return_data) #converts return statistics into dataframe
dfReturn = dfReturn.drop(0,axis=1) #drops unneccessary column

dfReturn.columns = ['Player', 'Return_Rating','1st_Serve_Return_Pct', '2nd_Serve_Return_Pct','Return_Games_Won_Pct','Break_Points_Won_Pct'] #creates header titles for return stats


firstServeReturnPct = dfReturn['1st_Serve_Return_Pct'].astype(str)
firstServeReturnPct = firstServeReturnPct.tolist()
firstServeReturnPct = [i.replace('%','') for i in firstServeReturnPct] #removes % sign from data in column so data can be used as numbers (not as string)

secondServeReturnPct = dfReturn['2nd_Serve_Return_Pct'].astype(str)
secondServeReturnPct = secondServeReturnPct.tolist()
secondServeReturnPct = [i.replace('%','') for i in secondServeReturnPct] #removes % sign from data


dfReturn['1st_Serve_Return_Pct'] = firstServeReturnPct
dfReturn['2nd_Serve_Return_Pct'] = secondServeReturnPct

dfReturn['1st_Serve_Return_Pct'] = pd.to_numeric(dfReturn['1st_Serve_Return_Pct']) #converts datatype to numeric
dfReturn['2nd_Serve_Return_Pct'] = pd.to_numeric(dfReturn['2nd_Serve_Return_Pct'])#converts datatype to numeric


#this method used the collected returning and serving stats for each player to determine two player's probability of winning a point on their serve in the given match. 
#the method takes in two strings of each players name in the match
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
    #formula for determining serving percentages below, takes into account various stats such as % first serves made, % first serves won when made, % second serve points won in addition to returning statistics
    #40 is used as a baseline and then added to according to each player's serving and returning statistics
    #it is probably important to consider double faulting percentages in order to make data after the first serve is missed more accurate. This is somewhat included in the % won on second serve stat but not completely. Return stats for second serve are irrelevant if there is a high double fault percentage, so an improved formula should account for this
    p1 = player1FirstServeProp.values*(player1FirstServeWon.values-(player2FirstServeReturnPct.values)) + player1SecondServeProp.values*(player1SecondServeWon.values-(player2SecondServeReturnPct.values)) + 40 
    p2 = player2FirstServeProp.values*(player2FirstServeWon.values-player1FirstServeReturnPct.values) + player2SecondServeProp.values*(player2SecondServeWon.values-player1SecondServeReturnPct.values) + 40

    #print(playerName1, p1) 
    #print(playerName2, p2)
    return(p1,p2)

#calculateServePct("Jaume Munar", "Tallon Griekspoor") 


