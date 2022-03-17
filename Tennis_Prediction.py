import random
import numpy as np
from numpy import ndarray

def gameSim(p):
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
        if (p1TBScore == 7 or p1TBScore == 8) and (p1TBScore - p2TBScore) >= 2:
            return 1
        elif (p2TBScore == 7 or p2TBScore == 8) and (p2TBScore - p1TBScore) >= 2:
            return 0
        else:
            return False

def tieBreakerSim(p1,p2, lastServer):
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
                if checkTieBreakWinner(p1Score, p2Score) == False:
                    if random.random() < p1:
                        p1Score += 1
                        currentServer = 2
                    else:
                        p2Score += 1
                        currentServer = 2
                else:
                    return checkTieBreakWinner(p1Score,p2Score)
        if currentServer == 2:
            for i in range(2):
                print(p1Score,p2Score)
                if checkTieBreakWinner(p1Score, p2Score) == False:
                    if random.random() < p2:
                        p2Score += 1
                        currentServer = 1
                    else:
                        p1Score += 1
                        currentServer = 1
                else:
                    return checkTieBreakWinner(p1Score,p2Score)
        while (p1Score + p2Score) > 14:
            if checkTieBreakWinner == False:
                p1Score -= 1
                p2Score -= 1
            else:
                break

def setSim(p1,p2,firstServer):
    p1Games = 0
    p2Games = 0
    currentServer = firstServer
    while True:

        if(currentServer == 1):
            print(p1Games, p2Games)
            gameWinner = gameSim(p1)
            if(gameWinner == 1):
                p1Games += 1
                currentServer = 2
            else:
                p2Games += 1
                currentServer = 2
          
        if(currentServer == 2):
            print(p1Games, p2Games)
            gameWinner = gameSim(p2)
            if(gameWinner == 0):
                p2Games += 1
                currentServer = 1
            else:
                p1Games += 1
                currentServer = 1
        
        if (p1Games == 6 or p1Games == 7) and (p1Games - p2Games) >=2:
            return 1
        
        if (p2Games == 6 or p1Games == 7) and (p2Games - p1Games) >=2:
            return 0
        
        if (p1Games == 6 and p2Games == 6):
            tieBreakResult = tieBreakerSim(p1,p2,firstServer)
            return tieBreakResult
        ## add tiebreaker 

        if (p1Games + p2Games) > 12:
            p1Games -= 1
            p2Games -= 1



        
            
print(tieBreakerSim(.5,.5,1))          


"""
n = 1000000   
x = ndarray((n,),int)
for i in range(n):
    x[i] = gameSim(.9)

#print(x)
p_hat = sum(x)/float(n)
sd = np.sqrt(p_hat*(1-p_hat)/float(n))

print ('The simulated probability is ', p_hat ,' with standard error ', sd, '\n')

"""
