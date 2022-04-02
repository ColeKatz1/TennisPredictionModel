# TennisPredictionModel

This project attempts to predict the outcome of tennis matches using a markov chain approach. The model simulates points, games, sets, tiebreakers, and finally the match given inputs of each player's estimated probability of winning a point on their serve. 

Files:

First, there is the Serving_Perctange.py file which takes data from https://www.atptour.com/en/stats/leaderboard?boardType=serve&timeFrame=52Week&surface=all&versusRank=all&formerNo1=false. The program takes serving and returning statistics for each player. Specifically, it takes this data for these players against the top 50 ranked players. For example, the % of first serve points won for Rafael Nadal against the top 50 tennis players. Ultimately, the program produces an estimated probability for each player winning a point on their serve given the specific matchup. These numbers are adjusted for the opponent by considering each player's serving and returning abilities.

Next, there is the Tennis_Prediction.py file which then simulates the matches n number of times. This program produces the probability that each player will win the match. It also produces the probability of each player winning a single game within the match in addition to the total estimated number of games played in the match. 
