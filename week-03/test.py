<<<<<<< HEAD
<<<<<<< HEAD
import pandas as pd
=======
import panda as pd
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992
=======
import panda as pd
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992
import numpy as np

df = pd.DataFrame()
df['name']=['Joey', 'Jeremy', 'Jenny']
df
<<<<<<< HEAD
<<<<<<< HEAD

df.assign (age = [28,33,27])

import os
os.chdir('week-03')

df = pd.read_csv('data/skyhook_2017-07.csv', sep=',')
df.head()
df.dtypes

df.shape
df.shape[0]
df.shape[1]
df.columns
type(df.columns)
df.cat_name
df.count
df['count']

df.lat.unique()
df.cat_name.unique()

df_multipleColumns = df[['hour', 'cat', 'count']]
df_multipleColumns.head()

df['hour']==158
time = df[df['hour']==158]
time.head
time.shape


 df[(df['hour']==158)&(df['count']>50)]

 bastille = df[df['date']=='2017-07-14']
 bastille.head
 bastille_enthusiasts = bastille[bastille['count']>bastille['count'].mean()]
bastille_enthusiasts.head
bastille_enthusiasts['count'].describe()
df.groupby('date')['count'].describe()

df.groupby(['date','hour'])['count'].describe()

df['count'].max()
df['count'].min()
df['count'].mean()
df['count'].std()
df['count'].count()

max_count = df['count'].max()
min_count = df['count'].min()
mean_count = df['count'].mean()

print (f"Maximum number of GPS pings:{max_count}")
print(f"Minimum number of GPS pings:{min_count}")
print(f"Average number of GPS pings :{mean_count}")
df[df['count'] == df['count'].max()]
df[df['count']==df['count'].min()]
df[df['count'].min()].groupby('hour')
df['count'].mean()


import matplotlib
%matplotlib inline

df['date_new']=pd.to_datetime(df['date'],format='%Y-%m-%d')
df['date'].head
df['weekday']=df['date_new'].apply(lambda x:x.weekday()+1)
df['weekday'].replace(7,0,inplace =True)

for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    ( (df['hour'] < j) & (df['hour'] > i + 18) ) |
    ( (df['hour'] > i + 18 ) & (df['hour'] < j) )
    )
    ].index, inplace = True)
  else:
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    (df['hour'] < j) | (df['hour'] > i + 18 )
    )
    ].index, inplace = True)

df.shape
import os
os.chdir('week-03')
df.to_csv('data/slyhook_cleaned.csv')
=======
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992
=======
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992
