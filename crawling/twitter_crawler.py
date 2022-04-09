# -*- coding: utf-8 -*-
import os
import json
import requests

from utils import save_json


# Load Twitter API secrets from an external JSON file
local_secrets_path = 'config/local_twitter_crawl_api_keys.json'
secrets = json.loads(open(local_secrets_path).read())
bearer_token = secrets['bearer_token']


def create_bearer_oauth_headers(bearer_token):
    headers = {'Authorization': 'Bearer {}'.format(bearer_token)}
    return headers


def create_url(keyword, max_results):
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#adding-a-query

    # One common query clause is -is:retweet, which will not match on Retweets,
    # thus matching only on original Tweets, Quote Tweets, and replies.

    # Query for english original tweets that contains a specific keyword
    if keyword.startswith('#'):  # encode the hashtag for url
        query = '%23{} -is:retweet lang:en'.format(keyword[1:])
    else:
        query = '{} -is:retweet lang:en'.format(keyword)
    tweet_fields = 'tweet.fields=author_id,created_at,geo,lang'
    # user_fields = 'user.fields=id,name,location'
    # expansions = 'expansions=author_id'
    url = 'https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}'.format(
        query,
        tweet_fields,
        # user_fields,
        # expansions,
        max_results
    )
    return url


def connect_to_endpoint(url, headers):
    response = requests.request('GET', url, headers=headers)
    # print(response.status_code)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception(response.status_code, response.text)
    return response.json()


def crawl_keyword(keyword, headers, max_results=100, num_pages=50):
    # The crawled corpus should have at least 10,000 records and at least 100,000 words.
    first_flag = True
    json_response = {}
    # max_results = 100  # per call(page)
    # num_pages = 10
    crawled_data = []  # collects the pages of data crawled into a list
    url = create_url(
        keyword,
        max_results
    )

    for _ in range(num_pages):
        if first_flag:
            next_url = url
            first_flag = False
        else:
            # A value that encodes the next 'page' of results that can be requested,
            # via the next_token request parameter.
            next_token = json_response['meta']['next_token']
            next_url = url + '&next_token=' + next_token

        try:
            json_response = connect_to_endpoint(next_url, headers)
        except requests.exceptions.RequestException as e:
            print('crawl_keyword ERROR!')
            print(e)

        # print(len(json_response['data']))
        # print(len(json_response['includes']['users']))

        if 'data' not in json_response:
            break

        crawled_data.extend(json_response['data'])

        metadata = json_response['meta']
        # there is no next page
        if 'next_token' not in metadata:
            break

    return crawled_data


def start_keyword_crawls(keywords, output_dir, headers):
    for keyword in keywords:
        keyword_data = {'keyword': keyword, 'data': []}
        print('Crawling keyword {}...'.format(keyword))
        crawled_data = crawl_keyword(keyword, headers)
        keyword_data['data'].extend(crawled_data)

        print()
        print('{} Records Crawled for keyword {}'.format(str(len(keyword_data['data'])), keyword))
        print('-' * 30)
        print()
        save_json(os.path.join(output_dir, '{}_crawled.json'.format(keyword)), keyword_data)


def main():
    try:
        headers = create_bearer_oauth_headers(bearer_token)

        # https://developer.twitter.com/en/docs/twitter-api/tweets/covid-19-stream/filtering-rules
        keywords = ['covid', 'coronavirus', '#wearamask',
                    'lockdown', '#lockdown',
                    '#pandemic', 'pandemic',
                    '#quarantine', 'quarantine',
                    '#remotework', '#remoteworking',
                    '#wfh', 'work from home', '#workfromhome', 'working from home', '#workingfromhome',
                    'social distancing', '#socialdistance', '#socialdistancing', '#socialdistancingnow']

        start_keyword_crawls(keywords=keywords, output_dir='crawled_data/', headers=headers)
    except Exception as e:
        print('[twitter_crawler]: Error in twitter_crawler.py!')
        print(e)


if __name__ == '__main__':
    main()
