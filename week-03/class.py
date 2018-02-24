import pandas as pd
import numpy as np

df= pd.DataFrame()
print(df)

df['name']=['Bilbo', 'Frodo', 'Samwise']

df
df.assign(height=[0.5,0.4,0.6])
#panda also includes bring in a data and store it into another data type
import os
os.chdir('week-03')
df= pd.read_csv('data/skyhook_2017-07.csv', sep=',')

df=pd.read_csv('data/skyhook_2017-07.csv', sep=',')
df.head()
df.shape[1]
df.columns
df['cat_name'].unique()
df['cat_name'].unique()
df['cat_name']
df.cat_name
df['hour'] ==158
one_fifty_eight= df[df('hour')==158]
#pass the dataframe to the , select star from DF where
one_fifty_eight.shape()
#we are only concerned where there are a lot of activities.
df['hour']==158
bastille = df[df['date']]=='2017-07-14'
bastille.head()
bastille['count']>bastille['count'].mean()
lovers_of_bastille.describe()

df['count'].max()
df['count'].min()
df['count'].mean()
df['count'].std()
df['count'].count()

df['hour'].unique()
jul_sec = df[df['date']]=='2017-07-02'
jul_sec.groupby('hour')['count'].sum().plot()


df['data_new']=pd.to_datetime(df['date'],format='%Y-%m-%d')# %Y indicates looking for four digits, same as the day and month
