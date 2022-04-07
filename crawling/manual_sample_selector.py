import json
import random

from utils import save_json


def add_sentiment_field(tweet):
    # -1: not labeled
    # 0 : negative
    # 2 : neutral
    # 4 : positive
    tweet['sentiment'] = -1
    return tweet


def main():
    # with open('cleaned_data/cleaned_data.json', 'r') as file:
    #     tweets = json.load(file)
    #     sampled_tweets = random.sample(tweets, 400)
    #     sampled_tweets = list(map(add_sentiment_field, sampled_tweets))
    #     print(len(sampled_tweets))
    #     save_json('cleaned_data/manually_label_samples_test.json', sampled_tweets)

    with open('cleaned_data/cleaned_data.json', 'r') as file:
        tweets = json.load(file)
        sampled_tweets = random.sample(tweets, 1000)
        sampled_tweets = list(map(add_sentiment_field, sampled_tweets))

        for i in range(5):  # 5 个人打标
            subset = sampled_tweets[i * 1000 // 5: (i + 1) * 1000 // 5]
            print(len(subset))
            save_json('cleaned_data/manually_label_samples_{}.json'.format(i), subset)


if __name__ == '__main__':
    main()
