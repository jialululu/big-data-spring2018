import jsonpickle
import tweepy
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret

auth = tweepy.AppAuthHandler
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def auth(key,secret):
    auth = tweepy.AppAuthHandler(key, secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
    else:
        return api

api = auth(api_key, api_secret)

def get_tweets(
    geo,
    out_file,
    search_term = '',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
          all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
          max_id = new_tweets[-1].id
          tweet_count += len(new_tweets)

    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  if write == True:
      all_tweets.to_json(out_file)
  return all_tweets

  # Set a Lat Lon

latlng = '42.359416,-71.093993' # Eric's office (ish)
  # Set a search distance
radius = '5mi'
  # See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
  # set output file location
file_name = 'data/tweets.json'
  # set threshold number of Tweets. Note that it's possible
  # to get more than one
t_max = 2000

def parse_tweet(tweet):
    p = pd.Series()
    if tweet.coordinates != None:
        p['lat'] = tweet.coordinates['coordinates'][0]
        p['lon'] = tweet.coordinates['coordinates'][1]
    else:
        p['lat'] = None
        p['lon'] = None
    p['location'] = tweet.user.location
    p['id'] = tweet.id_str
    p['content'] = tweet.text
    p['user'] = tweet.user.screen_name
    p['user_id'] = tweet.user.id_str
    p['time'] = str(tweet.created_at)
    return p

tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

tweets

tweets.dtypes
tweets['location'].unique()

loc_tweets = tweets[tweets['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets
df_count_tweets.columns
df_count_tweets.columns = ['count']
df_count_tweets

df_count_tweets.sort_index()


#clean up data
bos_list = tweets[tweets['location'].str.contains("Boston")]['location']
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list2 = tweets[tweets['location'].str.contains("boston")]['location']
tweets['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list3 = tweets[tweets['location'].str.contains("BOSTON")]['location']
tweets['location'].replace(bos_list3, 'Boston, MA', inplace = True)

atl_list = tweets[tweets['location'].str.contains("Atlanta")]['location']
tweets['location'].replace(atl_list, 'Atlanta, GA', inplace = True)

lon_list = tweets[tweets['location'].str.contains("London")]['location']
tweets['location'].replace(lon_list, 'London, United Kindom', inplace = True)

med_list = tweets[tweets['location'].str.contains("Medford")]['location']
tweets['location'].replace(med_list, 'Medford, MA', inplace = True)

hou_list = tweets[tweets['location'].str.contains("Houston")]['location']
tweets['location'].replace(hou_list, 'Houston, TX', inplace = True)

print(tweets['location'].unique())

#clean duplicates
tweets[tweets.duplicated(subset = 'content', keep = False)]
tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets.to_csv('twitterdata_pset3.csv', sep=',', encoding='utf-8')

colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

# 2.Create a pie chart
plt.pie(df_count_tweets['count'], labels=df_count_tweets.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.tight_layout()
plt.show()


#3.Create a scatterplot showing all of the tweets are that are geolocated
# Create a filter from df_tweets filtering only those that have values for lat and lon
tweets_geo = tweets[tweets['lon'].notnull() & tweets['lat'].notnull()]
len(tweets_geo)
len(tweets)

plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.show()
#only have 1 dot?





##Pick a search term

#4.search data term 'flood'
def get_tweets_floodsearch(
    geo,
    out_file,
    search_term = 'flood',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
          all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
          max_id = new_tweets[-1].id
          tweet_count += len(new_tweets)

    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  if write == True:
      all_tweets.to_json(out_file)
  return all_tweets

  latlng = '42.359416,-71.093993' # Eric's office (ish)
    # Set a search distance
  radius = '5mi'
    # See tweepy API reference for format specifications
  geocode_query = latlng + ',' + radius
    # set output file location
  file_name = 'data/tweets.json'
    # set threshold number of Tweets. Note that it's possible
    # to get more than one
  t_max = 2000

  tweets_flood = get_tweets_floodsearch(
    geo = geocode_query,
    tweet_max = t_max,
    write = True,
    out_file = file_name
  )

  tweets_flood

  tweets_flood.dtypes
  tweets_flood['location'].unique()

  loc_tweets_flood = tweets_flood[tweets_flood['location'] != '']
  count_tweets_flood = loc_tweets_flood.groupby('location')['id'].count()
  df_count_tweets_flood = count_tweets_flood.to_frame()
  df_count_tweets_flood
  df_count_tweets_flood.columns
  df_count_tweets_flood.columns = ['count']
  df_count_tweets_flood

  df_count_tweets_flood.sort_index()

#5.clean up data
bos_list_flood = tweets_flood[tweets_flood['location'].str.contains("Boston")]['location']
tweets_flood['location'].replace(bos_list_flood, 'Boston, MA', inplace = True)

bos_list_flood2 = tweets_flood[tweets_flood['location'].str.contains("boston")]['location']
tweets_flood['location'].replace(bos_list_flood2, 'Boston, MA', inplace = True)

bos_list_flood3 = tweets_flood[tweets_flood['location'].str.contains("BOSTON")]['location']
tweets_flood['location'].replace(bos_list_flood3, 'Boston, MA', inplace = True)

bos_list_flood4 = tweets_flood[tweets_flood['location'].str.contains("Bos")]['location']
tweets_flood['location'].replace(bos_list_flood4, 'Boston, MA', inplace = True)

mas_list_flood = tweets_flood[tweets_flood['location'].str.contains("Mass")]['location']
tweets_flood['location'].replace(mas_list_flood, 'Atlanta, GA', inplace = True)

new_list_flood = tweets_flood[tweets_flood['location'].str.contains("New England")]['location']
tweets_flood['location'].replace(new_list_flood, 'New England, MA', inplace = True)

sou_list_flood = tweets_flood[tweets_flood['location'].str.contains("South Boston")]['location']
tweets_flood['location'].replace(sou_list_flood, 'South Boston, MA', inplace = True)

print(tweets_flood['location'].unique())

#clean duplicates
tweets_flood[tweets_flood.duplicated(subset = 'content', keep = False)]
tweets_flood.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets_flood.to_csv('twitterdata_pset3_flood.csv', sep=',', encoding='utf-8')


#6.Create a scatterplot showing all of the tweets are that are geolocated
# Create a filter from df_tweets filtering only those that have values for lat and lon
tweets_flood_geo = tweets_flood[tweets_flood['lon'].notnull() & tweets_flood['lat'].notnull()]
len(tweets_flood_geo)
len(tweets_flood)

plt.scatter(tweets_flood_geo['lon'], tweets_flood_geo['lat'], s = 25)
plt.show()
