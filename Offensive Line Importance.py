
#PROJECT: DETERMINING THE IMPORTANCE OF THE OFFENSIVE LINE TO QB AND RB FANTASY PERFORMANCE

#--------------------------------------------------#

#Computation and Structuring:

import pandas as pd
import numpy as np
import scipy.stats as stats

#visualization:

import matplotlib.pyplot as plt

#modeling:

from sklearn.linear_model import LinearRegression

#--------------------------------------------------#

#DATA IMPORT AND STRUCTURING:

#read in files from directory

oline_scores = pd.read_csv('OLINE_scores.csv', sep=',')
player_stats = pd.read_csv('QB_RB_points.csv', sep=',')

print(player_stats.head())

team_score_avg = oline_scores.groupby('TEAM')['O_LINE_SCORE'].mean() #create average of o-line score for each team
team_score_sum = oline_scores.groupby('TEAM')['O_LINE_SCORE'].sum() #create a summed score across the oline by team

team_score_avg_df = pd.DataFrame(team_score_avg) #convert series to dataframe
team_score_avg_df['TEAM'] = team_score_avg_df.index #create joinable column from the index

team_score_sum_df = pd.DataFrame(team_score_sum) 
team_score_sum_df['TEAM'] = team_score_sum_df.index 

#merge player stats with oline_scores:

avg_all = pd.merge(player_stats, team_score_avg_df, left_on='TEAM', right_index=True, how='left',sort=False)
sum_all = pd.merge(player_stats, team_score_sum_df, left_on='TEAM', right_index=True, how='left',sort=False)

avg_all = avg_all.dropna(subset=['O_LINE_SCORE'])
avg_all_clean =  avg_all[avg_all['TEAM_x'] != 'CLEVELAND'] #dropped due to worst season in history of the NFL
avg_all_clean = avg_all_clean[avg_all_clean['TEAM_x'] != 'DENVER'] #quarter back committee and no consistent starter
avg_all_clean = avg_all_clean[avg_all_clean['TEAM_x'] != 'SEATTLE'] #Russell Wilson is a freak of nature
avg_all_clean = avg_all_clean[avg_all_clean['TEAM_x'] != 'CHICAGO'] #QB was a rookie, not very representative
avg_all_clean = avg_all_clean[avg_all_clean['TEAM_x'] != 'GREEN BAY'] #Aaron Rodgers season ending injury
avg_all_clean = avg_all_clean[avg_all_clean['TEAM_x'] != 'TEXANS'] #Deshaun Watson season ending injury

avg_all['TOTAL_RB_SCORE'] = avg_all['RB1_POINTS'] + avg_all['RB2_POINTS'].fillna(0)

#drop outliers for the RB points:

avg_all_RB = avg_all[avg_all['TEAM_x'] != 'NEW ORLEANS'] #large outlier skewing data

#--------------------------------------------------#

#INITIAL STATISTICAL ANALYSIS:

#Standard Deviation and ranges:

print(avg_all_clean['QB1_POINTS'].describe())  #39.72 std, 
print(avg_all['O_LINE_SCORE'].describe()) #max is 85 and min is 49, range is 36,  #9.36 std
print(avg_all_RB['TOTAL_RB_SCORE'].describe()) #66 std

#Correlation Matrices:

print(avg_all_clean.corr(method='pearson')) #cleaned for QB analysis
#shows a 0.31 correlation between o-line and QB performance 

print(avg_all.corr(method='pearson'))

#0.18 corr between oline and RB1 and 0.3 between oline and RB2
#RB1 and RB2 points are highly correlated at 0.6, so I will combine their points to create a total RB points column
#this should also control implicitly for a few things, 1) running back committees; and 2) partial seasons from injury or trade
#total RB Score yields a 0.42 correlation with o-line score


print(avg_all_RB.corr(method='pearson')) #correlation up to 0.52

#p-values:

print(stats.pearsonr(avg_all_clean['O_LINE_SCORE'], avg_all_clean['QB1_POINTS'])) #p-value is 0.1367, so not strong statistical significance
print(stats.pearsonr(avg_all['O_LINE_SCORE'], avg_all['TOTAL_RB_SCORE'])) #p-value is 0.023, so we can reject the null hypothesis and the relationship is significant
print(stats.pearsonr(avg_all_RB['O_LINE_SCORE'], avg_all_RB['TOTAL_RB_SCORE'])) #p-value is 0.0048, statistically significant

#--------------------------------------------------#

#MODELING AND VISUALIZATION

#Linear Regressions:

#average line performance basis:

X = avg_all['O_LINE_SCORE']
y = avg_all['QB1_POINTS']

X=X.reshape(len(X),1) #reshape X to array for lin reg input
y=y.reshape(len(y),1) #reshape y to array for lin reg input

lin_reg = LinearRegression()

lin_reg.fit(X, y)
print(lin_reg.score(X,y)) #r-squared calc...extremely low suggests no correlation between o-line composite and QB fantasy points

plt.scatter(X, y) #plots data in a scatter plot
plt.plot(X, lin_reg.predict(X), color='red',linewidth=3) #adds the linear regression LOBF
plt.show()

#With Outliers Removed:

X1 = avg_all_clean['O_LINE_SCORE']
y1 = avg_all_clean['QB1_POINTS']

X1=X1.reshape(len(X1),1) #reshape X to array for lin reg input
y1=y1.reshape(len(y1),1) #reshape y to array for lin reg input

lin_reg1 = LinearRegression()

lin_reg1.fit(X1, y1)
print(lin_reg1.score(X1,y1)) #r-squared goes up to 0.15, still low but some predictive power

plt.scatter(X1, y1) #plots data in a scatter plot
plt.plot(X1, lin_reg1.predict(X1), color='red',linewidth=3) #adds the linear regression LOBF
plt.show()

#For Running Backs:

#Total Team Set

X2 = avg_all['O_LINE_SCORE']
y2 = avg_all['TOTAL_RB_SCORE']

X2=X2.reshape(len(X2),1) #reshape X to array for lin reg input
y2=y2.reshape(len(y2),1) #reshape y to array for lin reg input

lin_reg2 = LinearRegression()

lin_reg2.fit(X2, y2)
print(lin_reg2.score(X2,y2)) #r-squared is 0.18

plt.scatter(X2, y2) #plots data in a scatter plot
plt.plot(X2, lin_reg1.predict(X2), color='red',linewidth=3) #adds the linear regression LOBF
plt.show()

#With outliers removed:

X3 = avg_all_RB['O_LINE_SCORE']
y3 = avg_all_RB['TOTAL_RB_SCORE']

X3=X3.reshape(len(X3),1) #reshape X to array for lin reg input
y3=y3.reshape(len(y3),1) #reshape y to array for lin reg input

lin_reg3 = LinearRegression()

lin_reg3.fit(X3, y3)
print(lin_reg3.score(X3,y3)) #r-squared is 0.27

plt.scatter(X3, y3) #plots data in a scatter plot
plt.plot(X3, lin_reg1.predict(X3), color='red',linewidth=3) #adds the linear regression LOBF
plt.show()

print(lin_reg3.coef_) 
print(lin_reg3.intercept_) 

#RB_SCORE = 3.58114785 * [O_LINE_SCORE]- 32.9
#coefficient strength not that high, possibly due to high dispersion/std of RB points (66)