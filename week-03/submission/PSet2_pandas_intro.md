<<<<<<< HEAD
# Problem Set 2: Intro to Pandas

Building off the in-class workshop, this problem set will require you to use some of Python's data wrangling functions and produce a few simple plots with Matplotlib. These plots will help us begin to think about how the aggregated GPS data works, how it might be useful, and how it might fall short.

## What to Submit

Create a duplicate of this file (`PSet2_pandas_intro.md`) in the provided 'submission' folder; your solutions to each problem should be included in the `python` code block sections beneath the 'Solution' heading in each problem section.

Be careful! We have to be able to run your code. This means that if you, for example, change a variable name and neglect to change every appearance of that name in your code, we're going to run into problems.

## Graphic Presentation

Make sure to label all the axes and add legends and units (where appropriate).

## Code Quality

While code performance and optimization won't count, all the code should be highly readable, and reusable. Where possible, create functions, build helper functions where needed, and make sure the code is self-explanatory.

## Preparing the Data

You'll want to make sure that your data is prepared using the procedure we followed in class. The code is reproduced below; you should simply be able to run the code and reproduce the dataset with well-formatted datetime dates and no erroneous hour values.

```python
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# This line lets us plot on our ipython notebook
%matplotlib inline

# Read in the data

df = pd.read_csv('week-03/data/skyhook_2017-07.csv', sep=',')

# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.
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
```

## Problem 1: Create a Bar Chart of Total Pings by Date

Your first task is to create a bar chart (not a line chart!) of the total count of GPS pings, collapsed by date. You'll have to use `.groupby` to collapse your table on the grouping variable and choose how to aggregate the `count` column. Your code should specify a color for the bar chart and your plot should have a title. Check out the [Pandas Visualization documentation](https://pandas.pydata.org/pandas-docs/stable/visualization.html) for some guidance regarding what parameters you can customize and what they do.

### Solution

```python

grp_df=df.groupby('date')['count'].sum()

grp_df.plot.bar(title='Total Pings by Date',color='y')


```

## Problem 2: Modify the Hours Column

Your second task is to further clean the data. While we've successfully cleaned our data in one way (ridding it of values that are outside the 24-hour window that correspond to a given day of the week) it will be helpful to restructure our `hour` column in such a way that hours are listed in a more familiar 24-hour range. To do this, you'll want to more or less copy the structure of the code we used to remove data from hours outside of a given day's 24-hour window. You'll then want to use the [DataFrame's `replace` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.replace.html). Note that you can use lists in both `to_replace` and `value`.

After running your code, you should have either a new column in your DataFrame or new values in the 'hour' column. These should range from 0-23. You can test this out in a couple ways; the simplest is probably to `df['hour'].unique()`; if you're interested in seeing sums of total pings by hour, you can run `df.groupby('hour')['count'].sum()`.

### Solution

```python

for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  df['hour'].replace(range(j, j + 5, 1), range(-5, 0, 1), inplace=True)
  df['hour'].replace(range(i, i + 19, 1), range(0, 19, 1), inplace=True)
df
df['hour'].unique()
```

## Problem 3: Create a Timestamp Column

Now that you have both a date and a time (stored in a more familiar 24-hour range), you can combine them to make a single timestamp. Because the columns in a `pandas` DataFrames are vectorized, this is a relatively simple matter of addition, with a single catch: you'll need to use `pd.to_timedelta` to convert your hours columns to a duration.

### Solution

```python

df['time_stamp']=df['date_new']+pd.to_timedelta(df['hour'],unit='h')
df

```

## Problem 4: Create Two Line Charts of Activity by Hour

Create two more graphs. The first should be a **line plot** of **total activity** by your new `timestamp` field---in other words a line graph that displays the total number of GPS pings in each hour over the course of the week. The second should be a **bar chart** of **summed counts** by hours of the day---in other words, a bar chart displaying the sum of GPS pings occurring across locations for each of the day's 24 hours.

### Solution

```python
line_plot=df.groupby('time_stamp')['count'].sum()
line_plot.plot.line(title='Total Activity Counts By Date',color='b')

bar_char=df.groupby(['hour'])['count'].sum()
bar_char.plot.bar(title='Activity Counts in Different Hours During The Day', color='m')
```

## Problem 5: Create a Scatter Plot of Shaded by Activity

Pick three times (or time ranges) and use the latitude and longitude to produce scatterplots of each. In each of these scatterplots, the size of the dot should correspond to the number of GPS pings. Find the [Scatterplot documentation here](http://pandas.pydata.org/pandas-docs/version/0.19.1/visualization.html#scatter-plot). You may also want to look into how to specify a pandas Timestamp (e.g., pd.Timestamp) so that you can write a mask that will filter your DataFrame appropriately. Start with the [Timestamp documentation](https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timestamps-vs-time-spans)!

```python

graph1= df[df['time_stamp']==pd.Timestamp('2017-07-02 18:00:00')]
#question: why do i need to use pd.Timestamp to specify? using '2017---' without the function gets the same graph.
graph1.plot.scatter(x='lon',y='lat',s=df['count']*0.1)

graph2=df[df['time_stamp']==pd.Timestamp('2017-07-14 18:00:00')]
graph2.plot.scatter(x='lon',y='lat',s=df['count']*0.1)

graph3=df[df['time_stamp']==pd.Timestamp('2017-07-14 08:00:00')]
graph3.plot.scatter(x='lon', y='lat', s=df['count']*0.1)

```

## Problem 6: Analyze Your (Very) Preliminary Findings

For three of the visualizations you produced above, write a one or two paragraph analysis that identifies:

1. A phenomenon that the data make visible (for example, how location services are utilized over the course of a day and why this might by).

The last two graphs which reflect activity counts at different time on the same day reveal that in the morning, 8am, people were concentrated in the middle area, and at night a large number of people moved to one particular spot in the west. We can guess that the center of the area is more about working or living uses, while the place where the west dot and the south dots locate are more about entertainment. Compare the first two maps which reflect activity counts at the same time in a day on different dates, we can see on Jul 02, people are sparsely scattered except up above there is a horizontal line where people concentrate. On Jul 14, dots are aligned with streets, amd concentrate in different parts of the city, which indicates on these two days, different activities happened in different areas of the city.

2. A shortcoming in the completeness of the data that becomes obvious when it is visualized.

if the maps could have a satellite map as background or could have a layer of urban context beneath, the scattered dots would make more sense of how they are related to urban infrastructures.

3. How this data could help us identify vulnerabilities related to climate change in the greater Boston area.

The maps reveal the concentration of people during different time of a day and on different dates, which help us to analyze the load of local services. If we could compare the maps with flooding tier maps, we could know what places are facing the risk of flooding and also bear severe load of utility.
=======
# Problem Set 2: Intro to Pandas

Building off the in-class workshop, this problem set will require you to use some of Python's data wrangling functions and produce a few simple plots with Matplotlib. These plots will help us begin to think about how the aggregated GPS data works, how it might be useful, and how it might fall short.

## What to Submit

Create a duplicate of this file (`PSet2_pandas_intro.md`) in the provided 'submission' folder; your solutions to each problem should be included in the `python` code block sections beneath the 'Solution' heading in each problem section.

Be careful! We have to be able to run your code. This means that if you, for example, change a variable name and neglect to change every appearance of that name in your code, we're going to run into problems.

## Graphic Presentation

Make sure to label all the axes and add legends and units (where appropriate).

## Code Quality

While code performance and optimization won't count, all the code should be highly readable, and reusable. Where possible, create functions, build helper functions where needed, and make sure the code is self-explanatory.

## Preparing the Data

You'll want to make sure that your data is prepared using the procedure we followed in class. The code is reproduced below; you should simply be able to run the code and reproduce the dataset with well-formatted datetime dates and no erroneous hour values.

```python
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# This line lets us plot on our ipython notebook
%matplotlib inline

# Read in the data

df = pd.read_csv('week-03/data/skyhook_2017-07.csv', sep=',')

# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.
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
```

## Problem 1: Create a Bar Chart of Total Pings by Date

Your first task is to create a bar chart (not a line chart!) of the total count of GPS pings, collapsed by date. You'll have to use `.groupby` to collapse your table on the grouping variable and choose how to aggregate the `count` column. Your code should specify a color for the bar chart and your plot should have a title. Check out the [Pandas Visualization documentation](https://pandas.pydata.org/pandas-docs/stable/visualization.html) for some guidance regarding what parameters you can customize and what they do.

### Solution

```python

grp_df=df.groupby('date')['count'].sum()

grp_df.plot.bar(title='Total Pings by Date',color='y')


```

## Problem 2: Modify the Hours Column

Your second task is to further clean the data. While we've successfully cleaned our data in one way (ridding it of values that are outside the 24-hour window that correspond to a given day of the week) it will be helpful to restructure our `hour` column in such a way that hours are listed in a more familiar 24-hour range. To do this, you'll want to more or less copy the structure of the code we used to remove data from hours outside of a given day's 24-hour window. You'll then want to use the [DataFrame's `replace` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.replace.html). Note that you can use lists in both `to_replace` and `value`.

After running your code, you should have either a new column in your DataFrame or new values in the 'hour' column. These should range from 0-23. You can test this out in a couple ways; the simplest is probably to `df['hour'].unique()`; if you're interested in seeing sums of total pings by hour, you can run `df.groupby('hour')['count'].sum()`.

### Solution

```python

for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  df['hour'].replace(range(j, j + 5, 1), range(-5, 0, 1), inplace=True)
  df['hour'].replace(range(i, i + 19, 1), range(0, 19, 1), inplace=True)
df
df['hour'].unique()
```

## Problem 3: Create a Timestamp Column

Now that you have both a date and a time (stored in a more familiar 24-hour range), you can combine them to make a single timestamp. Because the columns in a `pandas` DataFrames are vectorized, this is a relatively simple matter of addition, with a single catch: you'll need to use `pd.to_timedelta` to convert your hours columns to a duration.

### Solution

```python

df['time_stamp']=df['date_new']+pd.to_timedelta(df['hour'],unit='h')
df

```

## Problem 4: Create Two Line Charts of Activity by Hour

Create two more graphs. The first should be a **line plot** of **total activity** by your new `timestamp` field---in other words a line graph that displays the total number of GPS pings in each hour over the course of the week. The second should be a **bar chart** of **summed counts** by hours of the day---in other words, a bar chart displaying the sum of GPS pings occurring across locations for each of the day's 24 hours.

### Solution

```python
line_plot=df.groupby('time_stamp')['count'].sum()
line_plot.plot.line(title='Total Activity Counts By Date',color='b')

bar_char=df.groupby(['hour'])['count'].sum()
bar_char.plot.bar(title='Activity Counts in Different Hours During The Day', color='m')
```

## Problem 5: Create a Scatter Plot of Shaded by Activity

Pick three times (or time ranges) and use the latitude and longitude to produce scatterplots of each. In each of these scatterplots, the size of the dot should correspond to the number of GPS pings. Find the [Scatterplot documentation here](http://pandas.pydata.org/pandas-docs/version/0.19.1/visualization.html#scatter-plot). You may also want to look into how to specify a pandas Timestamp (e.g., pd.Timestamp) so that you can write a mask that will filter your DataFrame appropriately. Start with the [Timestamp documentation](https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timestamps-vs-time-spans)!

```python

graph1= df[df['time_stamp']==pd.Timestamp('2017-07-02 18:00:00')]
#question: why do i need to use pd.Timestamp to specify? using '2017---' without the function gets the same graph.
graph1.plot.scatter(x='lon',y='lat',s=df['count']*0.1)

graph2=df[df['time_stamp']==pd.Timestamp('2017-07-14 18:00:00')]
graph2.plot.scatter(x='lon',y='lat',s=df['count']*0.1)

graph3=df[df['time_stamp']==pd.Timestamp('2017-07-14 08:00:00')]
graph3.plot.scatter(x='lon', y='lat', s=df['count']*0.1)

```

## Problem 6: Analyze Your (Very) Preliminary Findings

For three of the visualizations you produced above, write a one or two paragraph analysis that identifies:

1. A phenomenon that the data make visible (for example, how location services are utilized over the course of a day and why this might by).

The last two graphs which reflect activity counts at different time on the same day reveal that in the morning, 8am, people were concentrated in the middle area, and at night a large number of people moved to one particular spot in the west. We can guess that the center of the area is more about working or living uses, while the place where the west dot and the south dots locate are more about entertainment. Compare the first two maps which reflect activity counts at the same time in a day on different dates, we can see on Jul 02, people are sparsely scattered except up above there is a horizontal line where people concentrate. On Jul 14, dots are aligned with streets, amd concentrate in different parts of the city, which indicates on these two days, different activities happened in different areas of the city.

2. A shortcoming in the completeness of the data that becomes obvious when it is visualized.

if the maps could have a satellite map as background or could have a layer of urban context beneath, the scattered dots would make more sense of how they are related to urban infrastructures.

3. How this data could help us identify vulnerabilities related to climate change in the greater Boston area.

The maps reveal the concentration of people during different time of a day and on different dates, which help us to analyze the load of local services. If we could compare the maps with flooding tier maps, we could know what places are facing the risk of flooding and also bear severe load of utility.
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992