# TennisPredictionModel

This project attempts to predict the outcome of tennis matches using a markov chain approach. The model simulates points, games, sets, tiebreakers, and finally the match given inputs of each player's estimated probability of winning a point on their serve. 

# Files:

First, there is the Serving_Perctange.py file which takes data from https://www.atptour.com/en/stats/leaderboard?boardType=serve&timeFrame=52Week&surface=all&versusRank=all&formerNo1=false. The program takes serving and returning statistics for each player. Specifically, it takes this data for these players against the top 50 ranked players. For example, the % of first serve points won for Rafael Nadal against the top 50 tennis players. Ultimately, the program produces an estimated probability for each player winning a point on their serve given the specific matchup. These numbers are adjusted for the opponent by considering each player's serving and returning abilities.


Next, there is the Markov_Chain_Simulation.py file which then simulates the matches n number of times. This program produces the probability that each player will win the match. It also produces the probability of each player winning a single game within the match in addition to the total estimated number of games played in the match. 

Finally, I've just added the Machine_Learning_Prediction.py file which takes the dataset I have been creating using ongoing tennis tournaments to predict the winner using machine learning. Currently, it is using a logistic regression; however, it is possible that this changes. Additionally, although there are only 91 possible matches for it to be trained and tested on, it has acheived an accuracy of approximately 70% only using the elo's of each player in general and on the given surface. As more games are played and simulated, the gameSim variable will also be added to the model for prediction. 


# Results:

The model is currently being used to simulate the Monte Carlo Masters tournament and through the first three rounds has an accuracy of 71%.

The model was used to simulate the results starting from the round of 32 of the recent Indian Wells tournament of 2022. The model acheived an accuracy of approximately 70% for picking the winner of each match. 


# Future of the project:

In terms of ways in which the model can be improved, more statistics about each player will be added such as the ELO of each player coming into the match. Models using ELO as a basis for prediction have generally been the most successful in tennis prediction (the most successful models are about 70% accurate). In order to incorporate ELO for prediction, a machine learning model will need to be created. Variables that will likely be used are: Surface (Clay, Grass, etc.), ELO, SimProb (Probability of each player winning the match according to the simulations of Markov_Chain_Simulation.py. Unfortunately, due to a lack of archived data, I will be creating a new dataset in order to acheive this over the next few months. The columns for this dataset will include the variables used in prediction (Surface, ELO, SimProb) in addition to PlayerName and Winner (who won). A nueral network and logistic regression approach will be taken for this. The dataset will include matches starting from Indian Wells 2022 and extend into future tournaments.

Below is a screenshot of the new data being collected using the model which will be used for machine learning in the future for better prediction. (Elo data still needs to be filled out)

![Screenshot 2022-04-11 223026](https://user-images.githubusercontent.com/84477747/162887335-d57c8ccd-181e-435d-ad0d-d7dfcaa123df.jpg)

I am also thinking of including new variables. For example, I may add a variable "unexpectedGamesWonInTourney" which will give the difference between total games won and expected games won in a tournament. This will give an idea of how "hot" a player is in a tournament. It will help the model account for players that are on a streak, although on paper they may be slightly worse than another. Maybe this variable will help the model become more accurate for these scenarios. However, it is not currently clear how to formulate this value. It may be easier to make an "unexpectedMatchesWonInTourney" as this is a lot simpler although it may provide less information.

Finally, another variable I am considering adding is a "clutch" which will take under pressure rankings from the ATP website for each player which measures how well this player performs under pressure (for example, during break points or set points).

