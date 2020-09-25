# This script calcualtes the total scores for everyone using
# the summary outputs from the score_weekly.py

# %%
import pandas as pd
import numpy as np
from glob import glob
import os

# %%
# Make a list of all the files in the results folder with names
# starting with forecast and ending with week.csv
# For more information on glob refer to:
# https://www.earthdatascience.org/courses/intro-to-earth-data-science/
# Chapter 12 lesson 3
file_list = glob(os.path.join('../weekly_results', 'forecast_week*.csv'))
file_listB = glob(os.path.join('../weekly_results', 'bonus*.csv'))



# %%
# setup a dataframe with all zeros for the scoreboard
# use the first summary file to make the name index
temp = pd.read_csv(file_list[0], index_col='name')
scoreboard = pd.DataFrame(data = np.zeros((len(temp),2)), 
                          index = temp.index, 
                          columns=['regular', 'bonus'])

# %%
#calculate the scores
#loop through reading summaries and add in the regular points
for file in file_list:
    print(file)
    temp=pd.read_csv(file, index_col='name')
    scoreboard['regular'] += temp['1week_points']+ temp['2week_points']

# Add in thte bonus points
for file in file_listB:
    print(file)
    temp=pd.read_csv(file, index_col='name')
    scoreboard['bonus'] += temp['points']


scoreboard['total'] = scoreboard['bonus'] + scoreboard['regular']


scoreboard['rank'] = scoreboard.total.rank(method='dense', ascending=False)
scoreboard = scoreboard.sort_values(by='total', ascending=False)
print(scoreboard)

