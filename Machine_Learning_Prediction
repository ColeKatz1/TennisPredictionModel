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


df = pandas.read_csv("C:/Users/colek/OneDrive/Desktop/ATP_Serve_Return_Stats/Tennis_Dataset.csv")




df['Elo_1_Combined'] = (df['elo_1'] + df['1_surface_elo'])/2
df['Elo_2_Combined'] = (df['elo_2'] + df['2_surface_elo'])/2

df['Elo_Combined_Diff'] = df['Elo_1_Combined']  - df['Elo_2_Combined']

df['Under_Pressure_Difference'] = df['1_pressure'] - df['2_pressure']

df['1_simProb'] = df['1_simProb'] - .5
df['1_simProb'] = df['1_simProb'] * 100
xAndY = df[['Player_1','Player_2','Elo_Combined_Diff','1_simProb','WinOrLoss','Under_Pressure_Difference']]
xAndY = xAndY.dropna(axis=0)
x = xAndY[['Elo_Combined_Diff','1_simProb']]#.values.reshape(-1,1)
y = xAndY['WinOrLoss']




count = 0
sum = 0
for i in range(1000):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.35)
    logistic = LogisticRegression()
    log_model = logistic.fit(x_train, y_train)
    score = log_model.score(x_test, y_test)
    predictions = log_model.predict(x_test)
    actual = y_test.values.tolist()
    
    

fpr, tpr, thresholds = metrics.roc_curve(y_test,predictions)
roc_auc = metrics.auc(fpr,tpr)
display = metrics.RocCurveDisplay(fpr = fpr,tpr = tpr,roc_auc = roc_auc)
display.plot()
plt.show()



    
    



#sum += score
#count += 1
#print(sum/count)
#print(log_model.coef_)
#PartialDependenceDisplay.from_estimator(log_model,x,[0],response_method='auto')
#PartialDependenceDisplay.from_estimator(log_model,x,[1],response_method='auto')
#PartialDependenceDisplay.from_estimator(log_model,x,[2],response_method='auto')
#plt.show()
#sum += score
#count += 1
#print(sum/count)


