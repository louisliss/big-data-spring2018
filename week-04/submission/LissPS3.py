##scraper

import jsonpickle
import tweepy
import pandas as pd
import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret

auth = tweepy.AppAuthHandler(api_key, api_secret)
# wait_on_rate_limit and wait_on_rate_limit_notify are options that tell our API object to automatically wait before passing additional queries if we come up against Twitter's wait limits (and to inform us when it's doing so).
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)


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

##search 1: no search term

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

tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

#resetting the dataframe
#tweets = pd.read_json('data/tweets.json')

##Cleaning the data

#Fixing locations

boston_loc = tweets[tweets['location'].str.contains("Boston", case=False)]['location']
tweets['location'].replace(boston_loc, 'Boston, MA', inplace = True)

cambridge_loc = tweets[tweets['location'].str.contains("Cambridge", case=False)]['location']
tweets['location'].replace(cambridge_loc, 'Cambridge, MA', inplace = True)

somerville_loc = tweets[tweets['location'].str.contains("Somerville", case=False)]['location']
tweets['location'].replace(somerville_loc, 'Somerville, MA', inplace = True)

medford_loc = tweets[tweets['location'].str.contains("Medford", case=False)]['location']
tweets['location'].replace(medford_loc, 'Medford, MA', inplace = True)

otherlist = tweets[~tweets['location'].str.contains('Boston, MA|Cambridge, MA|Somerville, MA|Medford, MA')]['location']
tweets['location'].replace(otherlist, 'Other Locations',inplace = True)

#dropping Duplicates

tweets[tweets.duplicated(subset = 'content', keep = False)]
tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)


##location pie chart

import matplotlib.pyplot as plt
%matplotlib inline

loc_tweets = tweets[tweets['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets
df_count_tweets.columns
df_count_tweets.columns = ['count']
df_count_tweets

df_count_tweets.sort_index()
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

plt.pie(df_count_tweets['count'], labels=df_count_tweets.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.title('Breakdown of User-Provided Locations')
plt.tight_layout()
plt.show()


##scatterplot

x = tweets['lon']
y = tweets['lat']

plt.scatter(x, y)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

title = "Location of Geocoded Tweets near Building 9, MIT"
subtitle = "Note: There was only a small subset of tweets with user-elected geocoding"

plt.suptitle(title, y=1.00, fontsize=18)
plt.title(subtitle, fontsize=10)
plt.show()

##search 2: using search term

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/climtweets.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 2000
search = "storm"

climtweets = get_tweets(
  geo = geocode_query,
  search_term = search,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)


#resetting the dataframe
climtweets = pd.read_json('data/climtweets.json')


##Cleaning the data

#Fixing locations

boston_loc = climtweets[climtweets['location'].str.contains("Boston", case=False)]['location']
climtweets['location'].replace(boston_loc, 'Boston, MA', inplace = True)

cambridge_loc = climtweets[climtweets['location'].str.contains("Cambridge", case=False)]['location']
climtweets['location'].replace(cambridge_loc, 'Cambridge, MA', inplace = True)

somerville_loc = climtweets[climtweets['location'].str.contains("Somerville", case=False)]['location']
climtweets['location'].replace(somerville_loc, 'Somerville, MA', inplace = True)

medford_loc = climtweets[climtweets['location'].str.contains("Medford", case=False)]['location']
climtweets['location'].replace(medford_loc, 'Medford, MA', inplace = True)

otherlist = climtweets[~climtweets['location'].str.contains('Boston, MA|Cambridge, MA|Somerville, MA|Medford, MA')]['location']
climtweets['location'].replace(otherlist, 'Other Locations',inplace = True)

#dropping Duplicates

climtweets[climtweets.duplicated(subset = 'content', keep = False)]
climtweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

##scatterplot part two

x = tweets['lon']
y = tweets['lat']

plt.scatter(x, y)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

title = "Location of Geocoded Tweets Mentioning 'Storm' near Building 9, MIT"
subtitle = "Note: There was only a small subset of tweets with user-elected geocoding"

plt.suptitle(title, y=1.00, fontsize=18)
plt.title(subtitle, fontsize=10)
plt.show()



##export

tweets.to_csv("C:/Users/Louis Liss/Desktop/github/big-data-spring2018/week-04/submission/tweets.csv")
climtweets.to_csv("C:/Users/Louis Liss/Desktop/github/big-data-spring2018/week-04/submission/climtweets.csv")
