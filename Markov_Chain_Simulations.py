from cmath import nan
from contextlib import nullcontext
import random
import numpy as np
from numpy import ndarray
import time
import pandas as pd
from ATP_Web_Scraper import calculateServePct
p1TotGamesWon = 0
p2TotGamesWon = 0
totGamesPlayed = 0
#this method simulates a game of tennis by simulating each point
def gameSim(p): 
    player1Score = 0
    player2Score = 0
    while True:
        if random.random() < p: #simulates a point given a probability (p) for the player winning the point
            player1Score += 1
        else:
            player2Score += 1
        if player1Score == 4 and (player1Score-player2Score) >=2: #checks if the game is won by player1
            return 1
        elif player2Score == 4 and (player2Score-player1Score) >=2: #checks if secondplayer has won the game
            return 0
        if (player1Score + player2Score) > 6: #need to rethink this, should reset the game at duece
                player1Score -= 1
                player2Score -= 1

#this method checks if there is a winner to the tiebreak
def checkTieBreakWinner(p1TBScore, p2TBScore):
    if (p1TBScore >= 7) and (p1TBScore - p2TBScore) >= 2: #checks for player1 winner, returns 1 if player1 won
        return 1
    if (p2TBScore >= 7) and (p2TBScore - p1TBScore) >= 2: #checks for player2 winner, returns 0 if player2 won
        return 0
    else:
        return -1 #otherwise, returns -1 if no winner yet

#this method simulates a tiebreaker to 7 
def tieBreakerSim(p1,p2, lastServer): 
    p1Score = 0
    p2Score = 0
    currentServer = lastServer #sets server to last server

    if(currentServer == 1): #then, changes the server as the tiebreak starts with a new server
        currentServer = 2
    else:
        currentServer = 1

    #this code chunk simulates the first point of the tiebreaker, it is separate as the first server only serves once. Each player serves twice after this
    if currentServer == 1: 
        if random.random() < p1:
            p1Score += 1
            currentServer = 2
        else:
            p2Score += 1
            currentServer = 2
    else:
        if random.random() < p2:
            p2Score += 1
            currentServer = 1
        else:
            p1Score += 1
            currentServer = 1


    #print(p1Score,p2Score)

    while True:
        
        if currentServer == 1:
            for i in range(2): #does this for 2 points
                #print(p1Score,p2Score)
                if (checkTieBreakWinner(p1Score, p2Score) != 0) and (checkTieBreakWinner(p1Score, p2Score) != 1): #checks if there is a winner to the tiebreak
                    if random.random() < p1: #if no winner, it simulates a point
                        p1Score += 1
                        currentServer = 2
                    else:
                        p2Score += 1
                        currentServer = 2
                else:
                    #print("")
                    return checkTieBreakWinner(p1Score,p2Score) #if there is a winner, it returns the winner
        if currentServer == 2:
            for i in range(2): #does this for 2 points for player2 serving 
                #print(p1Score,p2Score)
                if (checkTieBreakWinner(p1Score, p2Score)) != 0 and (checkTieBreakWinner(p1Score, p2Score) != 1): #checks if winner to tiebreak
                    if random.random() < p2: #if not, simulates point with player2 serving
                        p2Score += 1
                        currentServer = 1
                    else:
                        p1Score += 1
                        currentServer = 1
                else:
                    #print("")
                    return checkTieBreakWinner(p1Score,p2Score) #if there is a winner, it returns that winner

#this method checks if there is a winner to the set
def checkSetWinner(p1SetScore,p2SetScore):
        p1TotSets = 0
        p2TotSets = 0
        if (p1SetScore >= 6) and (p1SetScore - p2SetScore) >=2: #checks if player1 has won the set, returns 1 if yes
            return 1
        
        if (p2SetScore >= 6) and (p2SetScore - p1SetScore) >=2: #checks if player2 has won the set, returns 0 if yes
            return 0
        else:
            return -1 #returns -1 if no winner yet

#this method simulates a set
def setSim(p1,p2,firstServer):
    p1Games = 0
    p2Games = 0
    global p1TotGamesWon
    global p2TotGamesWon
    global totGamesPlayed
    currentServer = firstServer
    while True:
        
        if (p1Games == 6 and p2Games == 6): #if the score is 6-6, a tiebreaker is simulated
            tieBreakWinner = tieBreakerSim(p1,p2,currentServer)
            if tieBreakWinner == 1:
                p1TotGamesWon += 1
                totGamesPlayed += 1
            else:
                p2TotGamesWon += 1
                totGamesPlayed += 1
            return tieBreakWinner #returns winner of tiebreak as winner of the set
            

        if(currentServer == 1):
            if (checkSetWinner(p1Games, p2Games)) != 0 and (checkSetWinner(p1Games, p2Games) != 1): #checks if there is a winner of the set
                gameWinner = gameSim(p1) #if not, simulates the next game in the set
                if(gameWinner == 1):
                    p1Games += 1
                    p1TotGamesWon += 1
                    totGamesPlayed += 1
                    currentServer = 2
                else:
                    p2Games += 1
                    p2TotGamesWon += 1
                    totGamesPlayed += 1
                    currentServer = 2
            else:
                #print("")
                return checkSetWinner(p1Games,p2Games) #if there is a winner, it returns the winner
        
        #print(p1Games, p2Games)
        
        if (p1Games == 6 and p2Games == 6): #does another check of score 6-6, necessary to avoid scores of 8-6, so we must have this check here as well
            tieBreakWinner = tieBreakerSim(p1,p2,currentServer)
            if tieBreakWinner == 1:
                p1TotGamesWon += 1
                totGamesPlayed += 1
            else:
                p2TotGamesWon += 1
                totGamesPlayed += 1
            return tieBreakWinner

        #print(p1Games, p2Games)

        if (checkSetWinner(p1Games, p2Games)) != 0 and (checkSetWinner(p1Games, p2Games) != 1): #checks if set has a winner
            if(currentServer == 2):
                gameWinner = gameSim(p2) #if not, simulates the next game with player2 serving
                if(gameWinner == 1):
                    p2Games += 1
                    p2TotGamesWon += 1
                    totGamesPlayed += 1
                    currentServer = 1
                else:
                    p1Games += 1
                    p1TotGamesWon += 1
                    totGamesPlayed += 1
                    currentServer = 1
        else:
            #print("")
            return checkSetWinner(p1Games, p2Games) #if the set has a winner, it returns the winner
        
        #print(p1Games, p2Games)
        
        
    

#this method simulates a set without a tiebreaker (this means the set can have a score of 18-16 games). In some tournaments, this is how the final set is played (with no tiebreaker)
def finalSetSim(p1,p2,server):
    global p1TotGamesWon
    global p2TotGamesWon
    global totGamesPlayed
    p1Games = 0
    p2Games = 0
    currentServer = server

    #same process as setsim, only difference is that it does not run at tiebreaker at game score 6-6
    while True:
        
        if(currentServer == 1):
            if (checkSetWinner(p1Games, p2Games)) != 0 and (checkSetWinner(p1Games, p2Games) != 1):
                gameWinner = gameSim(p1)
                if(gameWinner == 1):
                    p1Games += 1
                    p1TotGamesWon += 1
                    totGamesPlayed += 1
                    currentServer = 2
                else:
                    p2Games += 1
                    p2TotGamesWon += 1
                    totGamesPlayed += 1
                    currentServer = 2
            else:
                #print(p1Games, p2Games)
                #print("")
                return checkSetWinner(p1Games,p2Games)
        
    
        
        
        
        if (checkSetWinner(p1Games, p2Games)) != 0 and (checkSetWinner(p1Games, p2Games) != 1):
            if(currentServer == 2):
                gameWinner = gameSim(p2)
                if(gameWinner == 1):
                    p2Games += 1
                    p2TotGamesWon += 1
                    totGamesPlayed += 1
                    currentServer = 1
                else:
                    p1Games += 1
                    p1TotGamesWon += 1
                    totGamesPlayed += 1
                    currentServer = 1
        else:
            #print(p1Games, p2Games)
            #print("")
            return checkSetWinner(p1Games, p2Games)
        
        #print(p1Games, p2Games)
        

#this method checks if there is a winner of the match and who won if there is a winner
def checkMatchWinner(p1Sets,p2Sets, setsToWin):
        if (p1Sets == setsToWin): #checks if player 1 has won, returns 1 if true
            return 1
        
        if (p2Sets == setsToWin): #checks if player2 has won, returns 0 if true
            return 0
        else:
            return -1 #returns -1 if no winner yet


def matchSim(p1,p2,firstServer,setsToWin, bestOf):
    p1Sets = 0
    p2Sets = 0
    p1TotSets = 0
    p2TotSets = 0
    currentServer = firstServer
    for i in range(bestOf): #will do this a max number of times equal to the maximum number of possible sets
        if (checkMatchWinner(p1Sets, p2Sets,setsToWin)) != 0 and (checkMatchWinner(p1Sets, p2Sets,setsToWin) != 1): #checks for winner of the match
            setWinner = setSim(p1,p2,currentServer) #simulates the next set if no winner yet
            if setWinner == 1:
                p1Sets += 1
                if currentServer == 1:
                    currentServer = 2
                else:
                    currentServer = 1
            else:
                p2Sets += 1
                if currentServer == 1:
                    currentServer = 2
                else:
                    currentServer = 1
        else:
            return checkMatchWinner(p1Sets,p2Sets, setsToWin) #if there is a match winner, returns the winner
        if p1Sets == setsToWin - 1 and p2Sets == setsToWin - 1: #if the next set determines the winner of match, it runs the finalsetsim which has no tiebreaker for the final set
            return finalSetSim(p1,p2,currentServer) #finalSetSim is for tournaments with the no tiebreaker in the final set rule

#this method simulates the match according to the rules that there is a tiebreak in the final set
def matchSimTiebreak(p1,p2,firstServer,setsToWin, bestOf):
    p1Sets = 0
    p2Sets = 0
    p1TotSets = 0
    p2TotSets = 0
    currentServer = firstServer
    for i in range(bestOf): #does this a maximum number of times equal to the maximum number of sets possible to be played
        if (checkMatchWinner(p1Sets, p2Sets,setsToWin)) != 0 and (checkMatchWinner(p1Sets, p2Sets,setsToWin) != 1): #checks for winner of match
            setWinner = setSim(p1,p2,currentServer) #simulates the next set
            if setWinner == 1:
                p1Sets += 1
                if currentServer == 1:
                    currentServer = 2
                else:
                    currentServer = 1
            else:
                p2Sets += 1
                if currentServer == 1:
                    currentServer = 2
                else:
                    currentServer = 1
        else:
            return checkMatchWinner(p1Sets,p2Sets, setsToWin) #if there is a winner to the match, returns the winner
        if p1Sets == setsToWin - 1 and p2Sets == setsToWin - 1: #checks if entering into the final set
            return setSim(p1,p2,currentServer) #returns the winner of the final, deciding set

#this method simulates the match n number of times given the rule that the final set does not include a tiebreaker at 6-6 (it is played until one player has 2 more games than the otehr after 6-6)
def matchSimNTimes(p1,p2,firstServer,setsToWin,bestOf,n):
    matchData = []
    p1Wins = 0
    totMatches = 0
    for i in range(n): #does this n number of times
        matchData+=[matchSim(p1,p2,firstServer,setsToWin,bestOf)] #adds the result of match sim to list
    for j in range(n): #goes through matchData list
        if matchData[j] == 1: #checks if the winner is player 1
            p1Wins += 1
            totMatches += 1
        else:
            totMatches += 1
    return p1Wins/totMatches #returns the proportion of times that player1 wins (the probability that player1 wins the match according to our simulation)

#this method simulates the match n number of times given the rule that the final set can include a tiebreaker at 6-6
def matchSimTiebreakNTimes(p1,p2,firstServer,setsToWin,bestOf,n):
    matchData = []
    p1Wins = 0
    totMatches = 0
    for i in range(n):
        matchData+=[matchSimTiebreak(p1,p2,firstServer,setsToWin,bestOf)]
    for j in range(n):
        if matchData[j] == 1:
            p1Wins += 1
            totMatches += 1
        else:
            totMatches += 1
    return p1Wins/totMatches

#this method simulates a set n number of times, it is useful to see what the average number of games each player will win in each set is
def setSimNTimes(p1,p2,firstServer,n):
    matchData = []
    p1Wins = 0
    totSets = 0
    for i in range(n):
        matchData+=[setSim(p1,p2,firstServer)]
    for j in range(n):
        if matchData[j] == 1:
            p1Wins += 1
            totSets += 1
        else:
            totSets += 1
    return p1Wins/totSets

#this method will simulate all matches in a day, and put the outputs from this simulation into an excel spreadsheet that will be used for future prediction
def simAllMatches():
    #date = "4_10_22",
    est_p1_list = []
    est_p2_list = []
    player1_list = []
    player2_list = []
    simProb_1_list = []
    #allPlayer1 = ["Federico Delbonis","Andrey Rublev","Felix Auger-Aliassime","Emil Ruusuvuori","Marton Fucsovics","Casper Ruud","Taylor Fritz","David Goffin","Hubert Hurkacz","Lorenzo Sonego","Albert Ramos-Vinolas","Sebastian Korda","Hubert Hurkacz","Pablo Carreno Busta","Lorenzo Musetti","Laslo Djere","Alejandro Davidovich Fokina","Casper Ruud","Taylor Fritz","Andrey Rublev","Diego Schwartzman","Jannik Sinner","Grigor Dimitrov","Alejandro Davidovich Fokina","Stefanos Tsitsipas","Alejandro Davidovich Fokina","Alejandro Davidovich Fokina"]
    #allPlayer2 = ["Alexander Zverev","Alex de Minaur","Lorenzo Musetti","Jannik Sinner","Diego Schwartzman","Holger Rune","Marin Cilic","Daniel Evans","Pedro Martinez","Laslo Djere","Cameron Norrie","Carlos Alcaraz","Albert Ramos-Vinolas","Alexander Zverev","Diego Schwartzman","Stefanos Tsitsipas","David Goffin","Grigor Dimitrov","Sebastian Korda","Jannik Sinner","Stefanos Tsitsipas","Alexander Zverev","Hubert Hurkacz","Taylor Fritz","Alexander Zverev","Grigor Dimitrov","Stefanos Tsitsipas"]

    #allPlayer1 = ["Bernabe Zapata Miralles","Jaume Munar","Maxime Cressy","Hugo Grenier","Nicolas Alvarez Varona","Adrian Mannarino","Soonwoo Kwon","Lorenzo Musetti","Marcos Giron","Pablo Andujar","Hugo Dellien","Feliciano Lopez","Marton Fucsovics","Carlos Taberner","Lloyd Harris","Lorenzo Musetti","Cameron Norrie","Diego Schwartzman","Ilya Ivashka","Stefanos Tsitsipas","Federico Coria","Soonwoo Kwon","Nikoloz Basilashvili","Alex de Minaur","Carlos Taberner","Lloyd Harris","Alexander Bublik","Pablo Carreno Busta","Marton Fucsovics","Frances Tiafoe","Pablo Carreno Busta","Emil Ruusuvuori","Frances Tiafoe","Diego Schwartzman","Jaume Munar","Cameron Norrie","Alex de Minaur","Stefanos Tsitsipas","Stefanos Tsitsipas","Cameron Norrie","Pablo Carreno Busta","Diego Schwartzman","Diego Schwartzman","Carlos Alcaraz","Carlos Alcaraz"]
    #allPlayer2 = ["Tommy Robredo","Gian Marco Moroni","Elias Ymer","Mackenzie McDonald","Brandon Nakashima","Egor Gerasimov","Benoit Paire","Sebastian Baez","Federico Coria","Ugo Humbert","Manuel Guinard","Emil Ruusuvuori","Jordan Thompson","Sebastian Korda","Roberto Carballes Baena","Daniel Evans","Egor Gerasimov","Mackenzie McDonald","Pedro Martinez","Ilya Ivashka","Grigor Dimitrov","Carlos Alcaraz","Jaume Munar","Ugo Humbert","Felix Auger-Aliassime","Albert Ramos-Vinolas","Emil Ruusuvuori","Bernabe Zapata Miralles","Federico Delbonis","Hugo Dellien","Lorenzo Sonego","Casper Ruud","Felix Auger-Aliassime","Lorenzo Musetti","Carlos Alcaraz","Marton Fucsovics","Lloyd Harris","Grigor Dimitrov","Carlos Alcaraz","Alex de Minaur","Casper Ruud","Felix Auger-Aliassime","Pablo Carreno Busta","Alex de Minaur","Pablo Carreno Busta"]
   
    #allPlayer1 = ["Soonwoo Kwon","Pablo Andujar","Dusan Lajovic","Federico Coria","Pablo Cuevas","Lloyd Harris","Tommy Paul","Albert Ramos-Vinolas","Jiri Vesely","Joao Sousa","Benjamin Bonzi","Pierre-Hugues Herbert"]
    #allPlayer2 = ["Benoit Paire","Nuno Borges","Frances Tiafoe","Bernabe Zapata Miralles","Roberto Carballes Baena","Carlos Taberner","Richard Gasquet","Jordan Thompson","Hugo Dellien","Sebastian Baez","Dominic Thiem","Sebastian Korda"]
    
    allPlayer1 = ["Alejandro Davidovich Fokina","Albert Ramos-Vinolas","Nuno Borges","Pablo Cuevas","Benjamin Bonzi","Felix Auger-Aliassime","Sebastian Baez","Richard Gasquet","Felix Auger-Aliassime","Alejandro Davidovich Fokina","Richard Gasquet","Albert Ramos-Vinolas","Sebastian Korda","Sebastian Baez","Frances Tiafoe"]
    allPlayer2 = ["Bernabe Zapata Miralles","Soonwoo Kwon","Frances Tiafoe","Fernando Verdasco","Sebastian Korda","Carlos Taberner","Marin Cilic","Hugo Dellien","Sebastian Korda","Frances Tiafoe","Sebastian Baez","Fernando Verdasco","Frances Tiafoe","Albert Ramos-Vinolas","Sebastian Baez"]
    
    for i in range(len(allPlayer1)):

        servePct = calculateServePct(allPlayer1[i],allPlayer2[i])
        est_p1 = servePct[0]
        est_p2 = servePct[1]
        est_p1_list.append(est_p1)
        est_p2_list.append(est_p2)
        player1_list.append(allPlayer1[i])
        player2_list.append(allPlayer2[i])
        
    


    dfList = {'Player_1' : player1_list, 'Player_2' : player2_list, 'est_p1' : est_p1_list, 'est_p2' : est_p2_list}
    df = pd.DataFrame(dfList)

    df['est_p1'] = df['est_p1'].str.get(0)
    df['est_p2'] = df['est_p2'].str.get(0)
    
    df = df.dropna(axis = 0)
    player1_dropped_list = df['Player_1'].to_list()
    player2_dropped_list = df['Player_2'].to_list()
    est_p1_dropped_list = df['est_p1'].to_list()
    est_p2_dropped_list = df["est_p2"].to_list()


    
    for i in range(len(est_p1_dropped_list)):
        simProb = matchSimTiebreakNTimes(est_p1_dropped_list[i]/100, est_p2_dropped_list[i]/100,1,2,3,100000)
        simProb_1_list.append(simProb)

    
    dfList = {'Player_1' : player1_dropped_list, 'Player_2' : player2_dropped_list, 'est_p1' : est_p1_dropped_list, 'est_p2' : est_p2_dropped_list, '1_simProb' : simProb_1_list}
    df = pd.DataFrame(dfList)
    
    
    
    
    return df
    
    


a = simAllMatches()

print(a)

#a.to_csv('simulations4.csv')
#a = calculateServePct("Andrey Rublev", "Jannik Sinner")
#print(a)
#print(matchSimTiebreakNTimes(a[0]/100,a[1]/100,1,2,3,100000))


#print(p1TotGamesWon/100000)
#print(p2TotGamesWon/100000)
#print(totGamesPlayed/100000)
