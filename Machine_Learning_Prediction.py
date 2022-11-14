from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
import pandas
import numpy
from sklearn.tree import DecisionTreeClassifier
from sklearn.inspection import partial_dependence, PartialDependenceDisplay
import matplotlib.pyplot as plt
import random
from sklearn import metrics


df = pandas.read_csv("Tennis_Dataset.csv") #this reads in the created dataset




df['Elo_1_Combined'] = (df['elo_1'] + df['1_surface_elo'])/2 #this combines the player's surface elo and overall elo into one variable that averages the two
df['Elo_2_Combined'] = (df['elo_2'] + df['2_surface_elo'])/2 #this does the same as above but for player 2

df['Elo_Combined_Diff'] = df['Elo_1_Combined']  - df['Elo_2_Combined'] #this creates a new variable which is the difference between player 1 and player 2's combined elos

df['Under_Pressure_Difference'] = df['1_pressure'] - df['2_pressure'] #creation of under pressure difference variable

df['1_simProb'] = df['1_simProb'] - .5
df['1_simProb'] = df['1_simProb'] * 100
xAndY = df[['Player_1','Player_2','Elo_Combined_Diff','1_simProb','WinOrLoss','Under_Pressure_Difference']]
xAndY = xAndY.dropna(axis=0)
x = xAndY[['Elo_Combined_Diff','1_simProb']]#.values.reshape(-1,1)
y = xAndY['WinOrLoss']



#this splits data into training and testing, creates a logistic regression model, makes predictions, and outputs the accuracy score
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.35)
logistic = LogisticRegression()
log_model = logistic.fit(x_train, y_train)
score = log_model.score(x_test, y_test)
predictions = log_model.predict(x_test)
actual = y_test.values.tolist()
print(score) 
    
#this creates an ROC curve and visualizes it
fpr, tpr, thresholds = metrics.roc_curve(y_test,predictions)
roc_auc = metrics.auc(fpr,tpr)
display = metrics.RocCurveDisplay(fpr = fpr,tpr = tpr,roc_auc = roc_auc)
display.plot()
plt.show()



 


