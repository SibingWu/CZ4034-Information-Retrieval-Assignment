import os
import json

from utils import save_json


def main():
    tweets = {}

    for json_file in os.listdir('crawled_data/'):
        print('Cleaning file {}...'.format(json_file))

        with open(os.path.join('crawled_data', json_file), 'r') as file:
            crawled_data = json.load(file)
            keyword = crawled_data['keyword']
            crawled_tweets = crawled_data['data']
            for tweet in crawled_tweets:
                tweet_id = tweet['id']
                if tweet_id not in tweets.keys():
                    tweets[tweet_id] = tweet
                    tweet['keyword'] = [keyword]
                else:
                    tweets[tweet_id]['keyword'].append(keyword)

    cleaned_data = list(tweets.values())

    print('{} records in total!'.format(len(cleaned_data)))  # 66,862 records in total!

    save_json('cleaned_data/cleaned_data.json', cleaned_data)


if __name__ == '__main__':
    main()
