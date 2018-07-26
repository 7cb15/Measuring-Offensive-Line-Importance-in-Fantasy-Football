# Measuring-Offensive-Line-Importance-in-Fantasy-Football

Using simple linear regression techniques I explore the impact of Offensive Line scores and rankings to the subsequent performance of Quarterbacks and Running Backs. The data is for the 2017 season and measures QB and RB performance based on the number of fantasy points obtained over the season. 

After some qualitative assessments are made to control for outliers (e.g. removing the Cleveland Browns, who went 0-16, from the analysis), we find that there is no statistically significant relationship between QB fantasy performance and offensive line strength. The R2 values are low and p-values suggest weak evidence against the null hypothesis.

However, we find a fairly strong correlation between offensive line strength and running back performance, with strong correlations, significant p-values, a reasonable R2 performance. The relationship is improved when running back performance is aggregated to the team level (i.e. performance for all running backs is taken as a whole).

Further analysis would need to be done to understand the week-to-week impacts on fantasy performance. Another note is that this initial analysis has limited value for fantasy draft strategy on teams where there is no clear RB1 as a strong offensive line just indicates the team's stable of running backs will be collectively successful. Further analysis should control for the number of touches (i.e. running opportunities) given to each running back. 

Happy Drafting!
