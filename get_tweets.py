import tweepy
from tt_credentials import consumer_key, consumer_secret, access_secret, access_token
from tweepy import OAuth1UserHandler, API 

 
auth = OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_secret) 
api = API(auth, wait_on_rate_limit=True) 

# og query: "elu OR amigue OR ilu OR ile OR amigues OR todes -filter:retweets"
# more tweets query: "delu OR minhe OR aquelu OR filhe -filter:retweets" 
 
#query = "elu OR amigue OR ilu OR ile OR amigues OR todes -filter:retweets" 
query = "elu OR elus OR delu OR delus OR minhe OR aquelu OR amigue OR todes OR filhe OR namorade OR outre OR outres" 
#tweets = api.search_tweets(QUERY, tweet_mode="extended", count=20000, max_results=20000, lang="pt") 

f = open("elu_tweets.txt", "w")

for i in tweepy.Cursor(api.search_tweets, q = query, tweet_mode="extended", lang="pt").items(10000):
    f.write(i.full_text)
    f.write('\n')

f.close()