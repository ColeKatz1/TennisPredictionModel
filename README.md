# TennisPredictionModel

This project attempts to predict the outcome of tennis matches using a markov chain approach. The model simulates points, games, sets, tiebreakers, and finally the match given inputs of each player's estimated probability of winning a point on their serve. 

Files:

First, there is the Serving_Perctange.py file which takes data from https://www.atptour.com/en/stats/leaderboard?boardType=serve&timeFrame=52Week&surface=all&versusRank=all&formerNo1=false. The program takes serving and returning statistics for each player. Specifically, it takes this data for these players against the top 50 ranked players. For example, the % of first serve points won for Rafael Nadal against the top 50 tennis players. Ultimately, the program produces an estimated probability for each player winning a point on their serve given the specific matchup. These numbers are adjusted for the opponent by considering each player's serving and returning abilities.


Next, there is the Tennis_Prediction.py file which then simulates the matches n number of times. This program produces the probability that each player will win the match. It also produces the probability of each player winning a single game within the match in addition to the total estimated number of games played in the match. 

Results:

The model is currently being used to simulate the Monte Carlo Masters tournament and through the first three rounds has an accuracy of 71%.

The model was used to simulate the results starting from the round of 32 of the recent Indian Wells tournament of 2022. The model acheived an accuracy of approximately 70% for picking the winner of each match. 


Future of the project:

In terms of ways in which the model can be improved, more statistics about each player will be added such as the ELO of each player coming into the match. Models using ELO as a basis for prediction have generally been the most successful in tennis prediction (the most successful models are about 70% accurate). In order to incorporate ELO for prediction, a machine learning model will need to be created. Variables that will likely be used are: Surface (Clay, Grass, etc.), ELO, SimProb (Probability of each player winning the match according to the simulations of Tennis_Prediction.py. Unfortunately, due to a lack of archived data, I will be creating a new dataset in order to acheive this over the next few months. The columns for this dataset will include the variables used in prediction (Surface, ELO, SimProb) in addition to PlayerName and Winner (who won). A nueral network and logistic regression approach will be taken for this. The dataset will include matches starting from Indian Wells 2022 and extend into future tournaments.

Below is a screenshot of the new data being collected using the model which will be used for machine learning in the future for better prediction. (Elo data still needs to be filled out)

![Screenshot 2022-04-11 223026](https://user-images.githubusercontent.com/84477747/162887335-d57c8ccd-181e-435d-ad0d-d7dfcaa123df.jpg)

