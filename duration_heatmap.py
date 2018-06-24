import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

df_data = pd.read_pickle('data\small_set\small_set.pkl')

#Keep measurement locations that were active by removing NaNs
#And sort to group measurement locations and order by timestamp
data = df_data[np.isfinite(df_data['duration'])].sort_values(by=['id','timestamp'])

#Linear interpolate for durations that are -1
# fp = duration that are not -1
# xp = position of those durations in the list
# positions in the range that are not in xp will get interpolated by the function np.interp

fp = data[(data.duration > 0)].duration.values
xp = [i for i,x in enumerate(data.duration) if x > 0]
inter = np.interp(range(0,data.duration.size),np.transpose(xp),fp)

pd.options.mode.chained_assignment = None  # default='warn'
data['duration_interpolation'] = inter

#Show the interpolation for one of the measurement locations
#X = range(data[(data.id == 'RWS01_MONIBAS_0581hrr0137ra0')].duration.size)
#plt.figure(figsize=(18,10))
#plt.plot(X, data[(data.id == 'RWS01_MONIBAS_0581hrr0137ra0')].duration)
#plt.plot(X, data[(data.id == 'RWS01_MONIBAS_0581hrr0137ra0')].duration_interpolation)
#plt.show()

#calculate the median of the durations to get the duration during normal hours
df_median = data.groupby(['id']).median()[['duration_interpolation']]
df_median.columns = ['duration_interpolation_median']
df = pd.merge(data, df_median, right_index=True, left_on='id')

#calculate the deviation compared to the median
df['duration_deviation'] = df.duration_interpolation - df.duration_interpolation_median

df = df.pivot(index='timestamp', columns='id', values='duration_deviation').clip(-50, 50)

ax = sns.heatmap(df, center=0, xticklabels=False, yticklabels=False, cbar=False, cmap="YlGnBu")

plt.show()