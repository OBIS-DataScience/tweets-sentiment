# Import necessary libraries
import re
import tweepy
import csv
import pandas as pd
from textblob import TextBlob
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier

# Twitter API credentials
CONSUMER_KEY = 'c4cOOivpIx2u9----------'
CONSUMER_SECRET = 'ba7dQIGfAH0OMbkz6iVR5sq2e2i------'
ACCESS_TOKEN = '60263710-8ccRGLIH55ENveaLcVvam0j4kScM------'
ACCESS_TOKEN_SECRET = 'BGZ7AXmJ6dXIaQidtN2ZIUqMcT-------'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Sample status update
status = "Tweeting through Python scripts, Check! #python #twitter #tweepy #datascience"
api.update_status(status=status)

# List to store tweets
tweets = []

# Search for tweets with the #iPhoneX hashtag in English since December 1, 2017
for tweet in tweepy.Cursor(api.search, q="#iPhoneX", lang="en", since="2017-12-01").items():
    tweets.append(tweet)

# Display basic information about the extracted tweets
print("Number of tweets extracted: {}.\n".format(len(tweets)))
for tweet in tweets[:5]:
    print(tweet.text)
    print()

# Create a DataFrame to store the tweet text
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

# Display the first few rows of the DataFrame
data.head()

# Access tweet metadata
print(tweets[0].id)
print(tweets[0].created_at)
print(tweets[0].source)
print(tweets[0].favorite_count)
print(tweets[0].retweet_count)
print(tweets[0].geo)
print(tweets[0].coordinates)
print(tweets[0].entities)

# Add additional metadata columns to the DataFrame
data['len'] = np.array([len(tweet.text) for tweet in tweets])
data['ID'] = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])

# Display the updated DataFrame
data.head()

# Define a function to clean tweet text
def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# Define a function to tokenize, remove stop words, and perform stemming
def process_text(tweet):
    '''
    Tokenizes, removes stop words, and performs stemming on the tweet text.
    '''
    # Tokenization
    words = nltk.word_tokenize(tweet)
    # Remove stop words
    words = [word for word in words if word.lower() not in stopwords.words('english')]
    # Stemming using Porter Stemmer
    stemmer = nltk.PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return ' '.join(words)

# Define a function to analyze sentiment using TextBlob
def analyze_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using TextBlob.
    '''
    analysis = TextBlob(process_text(clean_tweet(tweet)))
    if analysis.sentiment.polarity > 0:
        return 1  # Positive sentiment
    elif analysis.sentiment.polarity == 0:
        return 0  # Neutral sentiment
    else:
        return -1  # Negative sentiment

# Apply sentiment analysis to each tweet and add the results to the DataFrame
data['Sentiment'] = np.array([analyze_sentiment(tweet) for tweet in data['Tweets'])

# Display the first 10 rows of the DataFrame with sentiment labels
data.head(10)

# Define a file path to save the DataFrame
FILE_PATH = "~/Downloads/Sentimental Analysis/Tweets_Sentiment.csv"

# Save the DataFrame to a CSV file
data.to_csv(FILE_PATH)

# Load the data from the saved CSV file
data = pd.read_csv('Tweets_Sentiment.csv')

# Display the first few rows of the loaded data
data.head()

# Select only the 'Tweets' and 'Sentiment' columns
data = data[['Tweets', 'Sentiment']]

# Display the first few rows of the DataFrame with selected columns
data.head()

# Split the dataset into train and test sets
train, test = train_test_split(data, test_size=0.1)

# Remove neutral sentiments
train = train[train.Sentiment != -1]

# Filter positive and negative tweets
train_pos = train[train['Sentiment'] == 1]
train_pos = train_pos['Tweets']
train_neg = train[train['Sentiment'] == 0]
train_neg = train_neg['Tweets']

# Create and display word clouds for positive and negative tweets
print("Positive words")
wordcloud_draw(train_pos, 'white')

print("Negative words")
wordcloud_draw(train_neg)

# Calculate the percentage of positive, neutral, and negative tweets
positive = [tweet for index, tweet in enumerate(data['Tweets']) if data['Sentiment'][index] > 0]
neutral = [tweet for index, tweet in enumerate(data['Tweets']) if data['Sentiment'][index] == 0]
negative = [tweet for index, tweet in enumerate(data['Tweets']) if data['Sentiment'][index] < 0]

print("Percentage of positive tweets: {}%".format(len(positive) * 100 / len(data['Tweets']))
print("Percentage of neutral tweets: {}%".format(len(neutral) * 100 / len(data['Tweets']))
print("Percentage of negative tweets: {}%".format(len(negative) * 100 / len(data['Tweets']))

# Extract and display content sources
sources = []
for source in data['Source']:
    if source not in sources:
        sources.append(source)

# Print the list of content sources
print("Creation of content sources:")
for source in sources:
    print("* {}".format(source))
