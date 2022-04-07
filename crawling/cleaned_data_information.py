import json


def main():
    with open('cleaned_data/cleaned_data.json', 'r') as file:
        tweets = json.load(file)
        num_of_records = len(tweets)

        words = []
        for tweet in tweets:
            text = tweet['text'].strip()
            # print(text)
            text_words = text.split() # split by space
            # print(text_words)
            words.extend(text_words)

        print('Num of Records: {}'.format(str(num_of_records)))
        print('Num of Words: {}'.format(str(len(words))))
        print('Num of Unique Words: {}'.format(str(len(set(words)))))


if __name__ == '__main__':
    main()
