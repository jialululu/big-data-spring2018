import jsonpickle
import tweepy
import pandas as pd

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
<<<<<<< HEAD
  all_tweets = pd.DataFrame()
=======
  # all_tweets = pd.DataFrame()
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992
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
<<<<<<< HEAD
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
=======
        # all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992
        if write == True:
            with open(out_file, 'w') as f:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
<<<<<<< HEAD
  return all_tweets
=======
  # return all_tweets
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '1mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/tweets.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 200

get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)


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

<<<<<<< HEAD
tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

df = pd.read_json('data/tweets.json')

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

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

# Create a list of colors (from iWantHue)
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

# Create a pie chart
plt.pie(df_count_tweets['count'], labels=df_count_tweets.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.tight_layout()
plt.show()

# View the plot

# Create a filter from df_tweets filtering only those that have values for lat and lon
tweets_geo = tweets[tweets['lon'].notnull() & tweets['lat'].notnull()]
len(tweets_geo)
len(tweets)

# Use a scatter plot to make a quick visualization of the data points
# N.B., WHEN I DID THIS, I ONLY HAD SIX OUT OF ABOUT 100 TWEETS!
plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.show()

bos_list = tweets[tweets['location'].str.contains("Boston")]['location']
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

tweets[tweets.duplicated(subset = 'content', keep = False)]

tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)
=======


  for i in range(6,368,24):
      j=range(0,168,1)[i-5]
      print(i,j)
      if (j>i):
          df['hour'].replace(range(i,i+19,1),range(5,24,1),inplace = True)
          df.('hour').replace()
      else:
          df('hour').replace(range(i,i+19,3),range(0,24,1),inplace = True)
>>>>>>> e145d517caffa88f8c8fadd20c5ff1aa4fb8a992
