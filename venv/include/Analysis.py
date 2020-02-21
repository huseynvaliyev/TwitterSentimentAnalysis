import twitter
import csv
import tkinter as tk

twitter_api = twitter.Api(consumer_key='1eopvYvNup45mk4ZI0GYmO3MU',
                          consumer_secret='vKBRthBxgmg4IL6tNzrMIXLrtjr897lMr1vqHbgLZx2EY0UE6L',
                          access_token_key='4590923133-k6exGZBMbB7rnf6kpqIjagzn9nGi54OuLNo4v92',
                          access_token_secret='iaRLeXtFhndBhjPHcBn1WnfGnV0zmLHWQlkjahU6MkKWX')


def pressed(entry):
    def BuildTestSet(search_keyword):
        try:
            tweets_fetched = twitter_api.GetSearch(search_keyword, count=100)

            print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + search_keyword)

            return [{"text": status.text, "label": None} for status in tweets_fetched]
        except:
            print("Unfortunately, something went wrong..")
            return None

    testDataSet = BuildTestSet(entry)

    trainingData = []
    with open('/Users/huseynvaliyev/PycharmProjects/TwitterSentimentAnalysis/venv/include/tweetDataFile.csv',
              'rt') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            trainingData.append({"text": row[0], "label": row[1]})

    testTrainingData = []
    with open('/Users/huseynvaliyev/PycharmProjects/TwitterSentimentAnalysis/venv/include/testTweet.csv',
              'rt') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            testTrainingData.append({"text": row[0], "label": row[1]})

    testTrainingData1 = []
    with open('/Users/huseynvaliyev/PycharmProjects/TwitterSentimentAnalysis/venv/include/testTweet.csv',
              'rt') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            testTrainingData1.append({row[1]})

    print(testTrainingData1)

    posititveR=0
    negativeR=0
    for x in testTrainingData1:
        if(x=={'positive'}):
            posititveR=posititveR+1
        else:
            negativeR=negativeR+1

    print(posititveR)
    print(negativeR)

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
    preprocessedTestTrainingSet = tweetProcessor.processTweets(testTrainingData)
    preprocessedTrainingSet = tweetProcessor.processTweets(trainingData)
    preprocessedTestSet = tweetProcessor.processTweets(testDataSet)
    print(preprocessedTrainingSet)
    print(preprocessedTestTrainingSet)
    print(preprocessedTestSet)

    import nltk

    def buildVocabulary(preprocessedTrainingData):
        all_words = []

        for (words, sentiment) in preprocessedTrainingData:
            all_words.extend(words)

        wordlist = nltk.FreqDist(all_words)
        word_features = wordlist.keys()

        return word_features

    def extract_features(tweet):
        tweet_words = set(tweet)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    # Now we can extract the features and train the classifier
    word_features = buildVocabulary(preprocessedTrainingSet)
    print("----------------------------------------------------1")
    print(word_features)
    trainingFeatures = nltk.classify.apply_features(extract_features, preprocessedTrainingSet)
    print("----------------------------------------------------2")
    print(trainingFeatures)
    print("----------------------------------------------------3")

    NBayesClassifier = nltk.NaiveBayesClassifier.train(trainingFeatures)
    print(NBayesClassifier)
    print("----------------------------------------------------4")

    NBResultLabelsTest = [NBayesClassifier.classify(extract_features(tweet[0])) for tweet in preprocessedTestTrainingSet]
    positiveTest = NBResultLabelsTest.count('positive')
    negativeTest = NBResultLabelsTest.count('negative')
    if(100 * (posititveR / positiveTest) < 100*(negativeR/negativeTest)):
        correct = 100 * (posititveR / positiveTest)
    else:
        correct = 100*(negativeR/negativeTest)

    print(100*(posititveR/positiveTest))
    print(100*(negativeR/negativeTest))


    print(NBResultLabelsTest)
    print("----------------------------------------------------5")

    NBResultLabels = [NBayesClassifier.classify(extract_features(tweet[0])) for tweet in preprocessedTestSet]
    print(NBResultLabels)
    print("----------------------------------------------------6")

    # get the majority vote

    positive = 100 * NBResultLabels.count('positive') / len(NBResultLabels)
    negative = 100 * NBResultLabels.count('negative') / len(NBResultLabels)

    label['text'] = "Accuracy:" + str(round(correct)) + "%" " Positive: " + str(positive) + "%" + \
                    " Negative: " + str(negative) + "%"

HEIGHT = 400
WIDTH = 500
window = tk.Tk()

window.title("Twitter Sentiment Analysis")

canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(window, bg="#80c1ff", bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Enter", font=40, command=lambda: pressed(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(window, bg="#80c1ff", bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor="n")

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

window.mainloop()

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
