import twitter
import pandas

twitter_api = twitter.Api(consumer_key='1eopvYvNup45mk4ZI0GYmO3MU',
                          consumer_secret='vKBRthBxgmg4IL6tNzrMIXLrtjr897lMr1vqHbgLZx2EY0UE6L',
                          access_token_key='4590923133-k6exGZBMbB7rnf6kpqIjagzn9nGi54OuLNo4v92',
                          access_token_secret='iaRLeXtFhndBhjPHcBn1WnfGnV0zmLHWQlkjahU6MkKWX')


def BuildTestSet(search_keyword):
    try:
        tweets_fetched = twitter_api.GetSearch(search_keyword, count=100)

        print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + search_keyword)

        return [{"text": status.text, "label": None} for status in tweets_fetched]
    except:
        print("Unfortunately, something went wrong..")
        return None


search_term = input("Enter a search keyword:")
testDataSet = BuildTestSet(search_term)

# Burda corpus.cvc'den datalarımı fetch ediyorum
"""
def buildTrainingSet(corpusFile, tweetDataFile):
    import csv
    import time

    corpus = []

    with open(corpusFile, 'rt') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            corpus.append({"tweet_id": row[2], "label": row[1], "topic": row[0]})

    rate_limit = 180
    sleep_time = 900 / 180

    trainingDataSet = []

    for tweet in corpus:
        try:
            status = twitter_api.GetStatus(tweet["tweet_id"])
            print("Tweet fetched" + status.text)
            tweet["text"] = status.text
            trainingDataSet.append(tweet)
            time.sleep(sleep_time)
        except:
            continue
    # Now we write them to the empty CSV file
    with open(tweetDataFile, 'wt') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")
        for tweet in trainingDataSet:
            try:
                linewriter.writerow([tweet["tweet_id"], tweet["text"], tweet["label"], tweet["topic"]])
            except Exception as e:
                print(e)
    return trainingDataSet


corpusFile = '/Users/huseynvaliyev/PycharmProjects/TwitterSentimentAnalysis/venv/include/corpus.csv'
tweetDataFile = '/Users/huseynvaliyev/PycharmProjects/TwitterSentimentAnalysis/venv/include/tweetDataFile.csv'

trainingData1 = buildTrainingSet(corpusFile, tweetDataFile)
"""

trainingData = pandas.read_csv('tweetDataFile.csv','text', 'label')

import re
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords


class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])

    def processTweets(self, list_of_tweets):
        processedTweets = []
        for tweet in list_of_tweets:
            processedTweets.append((self._processTweet(tweet["text"]), tweet["label"]))
        return processedTweets

    def _processTweet(self, tweet):
        tweet = tweet.lower()  # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
        tweet = word_tokenize(tweet)  # remove repeated characters (helloooooooo into hello)
        return [word for word in tweet if word not in self._stopwords]

tweetProcessor = PreProcessTweets()
preprocessedTrainingSet = tweetProcessor.processTweets(trainingData)
preprocessedTestSet = tweetProcessor.processTweets(testDataSet)
