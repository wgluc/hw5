from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data  # file that contains OAuth credentials
import nltk


## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth = auth)
#Code for OAuth ends
baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = {'screen_name': username, 'count': num_tweets}
response = requests.get(baseurl, params, auth=auth)
tweet_data = json.loads(response.text)
tweet_file = open('tweet.json', 'w')
tweet_file.write(json.dumps(tweet_data, indent = 2))
tweet_file.close()
#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params, auth = auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def params_unique_combination(baseurl, params):
    res = []
    for k in params.keys():
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "&".join(res)

def get_twitter_params(username, num_tweets):
    baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params_diction = {}
    params_diction['screen_name'] = username
    params_diction['count'] = num_tweets
    return make_request_using_cache(baseurl, params_diction)

all_tweet = ''
for tweet in tweet_data:
    all_tweet = all_tweet + ' ' + tweet['text']

    tokens = nltk.word_tokenize(all_tweet)
    freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and "http" not in token and "https" not in token and "RT" not in token)
    for word, frequency in freqDist.most_common(5):
        print(word + ' ' + str(frequency))



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
