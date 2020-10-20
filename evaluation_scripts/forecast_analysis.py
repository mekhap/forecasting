# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataretrieval.nwis as nwis
import os
import eval_functions as ef

# %%
forecast_week = 8   # week 8 (Lourdes/Alexa 10/19/20)

# %%
station_id = "09506000"

# list of students in the class
# get lists using functions in eval_functions.py
names = ef.getLastNames()
firstnames = ef.getFirstNames()
nstudent = len(names)

# get start and stop dates using functions in eval_functions.py
dates = ef.weekDates(forecast_week)
start_date = dates[0]
stop_date = dates[1]

print("Evaluating forecasts up to", start_date, 'To', stop_date)

# %%
# Setting up a list of week numbers to be used in plotting
weeks = []
for i in range(16):
    # this is done because python counts 1 behind
    weeks.append('week_' '%s' % (i+1))

# %%
# mamking two empty arrays to  hold the forecasts
forecasts_1 = np.zeros([nstudent, len(weeks)])  # 1wk forecast for this week
forecasts_2 = np.zeros([nstudent, len(weeks)])  # 2wk forecasts for this week

# Reading the individual student forecast csvs
# to populate the dataframe
for i in range(nstudent):
    filename = names[i] + '.csv'
    filepath = os.path.join('..', 'forecast_entries', filename)
    print(filepath)
    temp = pd.read_csv(filepath, index_col='Forecast #')
    for n in range(1, forecast_week+1):
        forecasts_1[i, n-1] = temp.loc[(n), '1week']
        forecasts_2[i, n-1] = temp.loc[(n), '2week']

# %%
# compiled into data frames you can use for graphing
weekly_forecast1w = pd.DataFrame({}, index=firstnames)
weekly_forecast2w = pd.DataFrame({}, index=firstnames)

for i in range(16):
    weekly_forecast1w.insert(i, 'week_%s' % (i+1), forecasts_1[:, i], True)
    weekly_forecast2w.insert(i, 'week_%s' % (i+1), forecasts_2[:, i], True)

# everything above this can be copied
# and pasted into your analysis

# %%
# Week 7 addition, create dataframe containing weekly flows
# NOTE: Must first run Get_Observations.py script
weekly_flows = pd.read_csv("../weekly_results/weekly_observations.csv")

# %% Week 7 addition, format new dataframes for
# weekly plotting, and assign same index
# trim and tanspose to make plotting easier
weekly_forecast1w_graph = weekly_forecast1w.iloc[:, 0:forecast_week-1].T
weekly_forecast2w_graph = weekly_forecast2w.iloc[:, 0:forecast_week-1].T
# trim and set index the same, weekly flow start 8/23
# while student forecasts start 8/30 so need to trim dataset
weekly_flows_graph = weekly_flows.iloc[1:forecast_week, 3:4]
weekly_flows_graph.set_index(weekly_forecast1w_graph.index,
                             append=False, inplace=True)


# %%
# Week 7 addition, plot timeseries of
# 1 week forecasts and observed weekly average flow
markers = ['o', 'v', '^', 'D', '>', 's', 'P', 'X', '<', '>',
           'X', 'o', 'v', 's', '^', 'P', '<', 'D', 's']
fig, ax = plt.subplots()
ax.plot(weekly_forecast1w_graph)
for i, line in enumerate(ax.get_lines()):
    line.set_marker(markers[i])
ax.plot(weekly_flows['observed'], color='black', marker='o',
        linestyle='--', linewidth=3)
ax.set(title="1 Week Forecast", xlabel="Week",
       ylabel="Weekly Avg Flow [cfs]",
       xlim=(0, forecast_week-2), ylim=(0, None))
# plt.xlim([0, forecast_week-1])
plot_labels = firstnames + ['Observed Flow']
ax.legend(plot_labels, loc='lower center',
          bbox_to_anchor=(.5, -0.4), ncol=5)
fig.set_size_inches(9, 5)
plt.show()
# fig.savefig("1Wk_Forecasts", bbox_inches='tight')


# %%
# Week 7 addition, plot timeseries of 1 week forecast error
Errow_1wk = weekly_forecast1w_graph.subtract(weekly_flows_graph['observed'],
                                             axis=0)

fig, ax = plt.subplots()
ax.plot(Errow_1wk)
for i, line in enumerate(ax.get_lines()):
    line.set_marker(markers[i])
plt.axhline(y=0, color='black', linestyle='--', linewidth=3)
ax.set(title="1 Week Forecast Error", xlabel="Week",
       ylabel="Deviation from Weekly Avg Flow [cfs]",
       xlim=(0, forecast_week-2), ylim=[-60, 60])
plot_labels = firstnames
ax.legend(plot_labels, loc='lower center',
          bbox_to_anchor=(.5, -0.4), ncol=5)
fig.set_size_inches(9, 5)
plt.show()
# fig.savefig("1Wk_Error", bbox_inches='tight')


# %%
# Week 7 addition, plot timeseries of
# 2 week forecasts and observed weekly average flow
fig, ax = plt.subplots()
ax.plot(weekly_forecast2w_graph)
for i, line in enumerate(ax.get_lines()):
    line.set_marker(markers[i])
ax.plot(weekly_flows['observed'], color='black', marker='o',
        linestyle='--', linewidth=3)
ax.set(title="2 Week Forecast", xlabel="Week",
       ylabel="Weekly Avg Flow [cfs]",
       xlim=(0, forecast_week-2), ylim=(0, None))
plot_labels = firstnames + ['Observed Flow']
ax.legend(plot_labels, loc='lower center',
          bbox_to_anchor=(.5, -0.4), ncol=5)
fig.set_size_inches(9, 5)
plt.show()
# fig.savefig("2Wk_Forecasts", bbox_inches='tight')

# %%
# Week 7 addition, plot timeseries of 2 week forecast error
Errow_2wk = weekly_forecast2w_graph.subtract(weekly_flows_graph['observed'],
                                             axis=0)

fig, ax = plt.subplots()
ax.plot(Errow_2wk)
for i, line in enumerate(ax.get_lines()):
    line.set_marker(markers[i])
plt.axhline(y=0, color='black', linestyle='--', linewidth=3)
ax.set(title="2 Week Forecast Error", xlabel="Week",
       ylabel="Deviation from Weekly Avg Flow [cfs]",
       xlim=(0, forecast_week - 2), ylim=[-60, 60])
plot_labels = firstnames
plt.xlim([0, forecast_week-2])
ax.legend(plot_labels, loc='lower center',
          bbox_to_anchor=(.5, -0.4), ncol=5)
fig.set_size_inches(9, 5)
plt.show()
# fig.savefig("2Wk_Error", bbox_inches='tight')


# %%
# helpful for graphing
weeks = []
for i in range(16):
    weeks.append('week_' '%s' % (i+2))
    # made because student forecasts start week 2

plt.style.use('seaborn-whitegrid')

plt.plot(weeks, weekly_forecast1w.mean(), marker='o',
         label='class average')
plt.plot(weeks, weekly_forecast1w.quantile(0.25), marker='o',
         label='lower quantile')
plt.plot(weeks, weekly_forecast1w.quantile(0.75), marker='o',
         label='upper quantile')
plt.plot(weeks, weekly_forecast1w.min(), marker='o',
         label='min')
plt.plot(weeks, weekly_forecast1w.max(), marker='o',
         label='max')
plt.plot(weeks[:15], weekly_flows['observed'][1:],
         color='black', marker='o', linestyle='--',
         label='observed')
plt.ylabel('Flow (cfs)')
plt.ylim([0, 1000])
plt.xlim([0, forecast_week-2])
plt.title('Weekly Discharge Prediction')
plt.xticks(rotation=45, fontsize=10)
plt.legend()

# %%
# week 7 plot

plt.style.use('seaborn-whitegrid')

plt.plot(weeks, weekly_forecast1w.mean(), marker='o',
         label='class average')
plt.plot(weeks, weekly_forecast1w.quantile(0.25), marker='o',
         label='lower quantile')
plt.plot(weeks, weekly_forecast1w.quantile(0.75), marker='o',
         label='upper quantile')
plt.plot(weeks, weekly_forecast1w.min(), marker='o',
         label='min')
plt.plot(weeks, weekly_forecast1w.max(), marker='o',
         label='max')
plt.plot(weeks[:15], weekly_flows['observed'][1:],
         color='black', marker='o', linestyle='--',
         label='observed')
plt.ylabel('Flow (cfs)')
plt.ylim([0, 150])
plt.xlim([0, forecast_week-2])
plt.title('Weekly Discharge Prediction')
plt.xticks(rotation=45, fontsize=10)
plt.legend()

# %%
# week 7 plot

plt.plot(weeks, weekly_forecast2w.mean(), marker='o',
         label='class average')
plt.plot(weeks, weekly_forecast2w.quantile(0.25), marker='o',
         label='lower quantile')
plt.plot(weeks, weekly_forecast2w.quantile(0.75), marker='o',
         label='upper quantile')
plt.plot(weeks, weekly_forecast2w.min(), marker='o',
         label='min')
plt.plot(weeks, weekly_forecast2w.max(), marker='o',
         label='max')
plt.plot(weeks[:14], weekly_flows['observed'][2:],
         color='black', marker='o', linestyle='--',
         label='observed')
plt.ylabel('Flow (cfs)')
plt.ylim([0, 150])
plt.xlim([0, forecast_week-2])
plt.title('Weekly Discharge Prediction')
plt.xticks(rotation=45, fontsize=10)
plt.legend()

# %%