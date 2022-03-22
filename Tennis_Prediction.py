import random
import numpy as np
from numpy import ndarray
import time
import pandas as pd
def gameSim(p): #consider making the model slightly more complicated by adding in 1st and second serves,
                #I have the stats on these so its very easy to do and to predict each of the stats. OVer the match, they will more or less even out
    player1Score = 0
    player2Score = 0
    pointCount = 0
    while True:
        if random.random() < p:
            player1Score += 1
            pointCount += 1
        else:
            player2Score += 1
            pointCount += 1
        if player1Score == 4 and (player1Score-player2Score) >=2:
            return 1
        elif player2Score == 4 and (player2Score-player1Score) >=2:
            return 0
        if (player1Score + player2Score) > 6:
                player1Score -= 1
                player2Score -= 1

def checkTieBreakWinner(p1TBScore, p2TBScore):
        if (p1TBScore >= 7) and (p1TBScore - p2TBScore) >= 2:
            return 1
        if (p2TBScore >= 7) and (p2TBScore - p1TBScore) >= 2:
            return 0
        else:
            return -1


def tieBreakerSim(p1,p2, lastServer): #make sure that it starts on the right server
    p1Score = 0
    p2Score = 0
    pointCount = 0
    currentServer = lastServer
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
    print(p1Score,p2Score)
    while True:
        
        if currentServer == 1:
            for i in range(2):
                print(p1Score,p2Score)
                if (checkTieBreakWinner(p1Score, p2Score) != 0) and (checkTieBreakWinner(p1Score, p2Score) != 1):
                    if random.random() < p1:
                        p1Score += 1
                        currentServer = 2
                    else:
                        p2Score += 1
                        currentServer = 2
                else:
                    print("")
                    return checkTieBreakWinner(p1Score,p2Score)
        if currentServer == 2:
            for i in range(2):
                print(p1Score,p2Score)
                if (checkTieBreakWinner(p1Score, p2Score)) != 0 and (checkTieBreakWinner(p1Score, p2Score) != 1):
                    if random.random() < p2:
                        p2Score += 1
                        currentServer = 1
                    else:
                        p1Score += 1
                        currentServer = 1
                else:
                    print("")
                    return checkTieBreakWinner(p1Score,p2Score)

def checkSetWinner(p1SetScore,p2SetScore):
        if (p1SetScore >= 6) and (p1SetScore - p2SetScore) >=2:
            return 1
        
        if (p2SetScore >= 6) and (p2SetScore - p1SetScore) >=2:
            return 0
        else:
            return -1

def setSim(p1,p2,firstServer):
    p1Games = 0
    p2Games = 0
    currentServer = firstServer
    while True:
        
        if (p1Games == 6 and p2Games == 6):
            return tieBreakerSim(p1,p2,currentServer) # need to make sure the tiebreaker starts with the correct server
            

        if(currentServer == 1):
            if (checkSetWinner(p1Games, p2Games)) != 0 and (checkSetWinner(p1Games, p2Games) != 1):
                gameWinner = gameSim(p1)
                if(gameWinner == 1):
                    p1Games += 1
                    currentServer = 2
                else:
                    p2Games += 1
                    currentServer = 2
            else:
                print("")
                return checkSetWinner(p1Games,p2Games)
        
        print(p1Games, p2Games)
        
        if (p1Games == 6 and p2Games == 6):
            return tieBreakerSim(p1,p2,currentServer)

        print(p1Games, p2Games)

        if (checkSetWinner(p1Games, p2Games)) != 0 and (checkSetWinner(p1Games, p2Games) != 1):
            if(currentServer == 2):
                gameWinner = gameSim(p2)
                if(gameWinner == 1):
                    p2Games += 1
                    currentServer = 1
                else:
                    p1Games += 1
                    currentServer = 1
        else:
            print("")
            return checkSetWinner(p1Games, p2Games)
        
        print(p1Games, p2Games)
        
        
    

def finalSetSim(p1,p2,server):
    p1Games = 0
    p2Games = 0
    currentServer = server
    while True:
        
        if(currentServer == 1):
            if (checkSetWinner(p1Games, p2Games)) != 0 and (checkSetWinner(p1Games, p2Games) != 1):
                gameWinner = gameSim(p1)
                if(gameWinner == 1):
                    p1Games += 1
                    currentServer = 2
                else:
                    p2Games += 1
                    currentServer = 2
            else:
                print(p1Games, p2Games)
                print("")
                return checkSetWinner(p1Games,p2Games)
        
    
        
        
        
        if (checkSetWinner(p1Games, p2Games)) != 0 and (checkSetWinner(p1Games, p2Games) != 1):
            if(currentServer == 2):
                gameWinner = gameSim(p2)
                if(gameWinner == 1):
                    p2Games += 1
                    currentServer = 1
                else:
                    p1Games += 1
                    currentServer = 1
        else:
            print(p1Games, p2Games)
            print("")
            return checkSetWinner(p1Games, p2Games)
        
        print(p1Games, p2Games)
        


def checkMatchWinner(p1Sets,p2Sets, setsToWin):
        if (p1Sets == setsToWin):
            return 1
        
        if (p2Sets == setsToWin):
            return 0
        else:
            return -1


def matchSim(p1,p2,firstServer,setsToWin, bestOf):
    p1Sets = 0
    p2Sets = 0
    currentServer = firstServer
    for i in range(bestOf):
        if (checkMatchWinner(p1Sets, p2Sets,setsToWin)) != 0 and (checkMatchWinner(p1Sets, p2Sets,setsToWin) != 1):
            setWinner = setSim(p1,p2,currentServer) #make sure you change firstserver with each set
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
            return checkMatchWinner(p1Sets,p2Sets, setsToWin)
        if p1Sets == setsToWin - 1 and p2Sets == setsToWin - 1:
            return finalSetSim(p1,p2,currentServer)
