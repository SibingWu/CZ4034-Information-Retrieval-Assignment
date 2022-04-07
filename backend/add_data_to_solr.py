import pandas as pd
import pysolr
import os


# def find(name, path):
#    for root, dirs, files in os.walk(path):
#        if name in files:
#            return os.path.join(root, name)


# Read the toxic tweet data from csv file
#directory = find("quarantine_crawled.json", ".")
#tweets = pd.read_json("cleaned_data.json", dtype={'id': str})

# Re-structure raw data for indexing
# data = [{"id": index, "tweet": row["text"], "user_location": row["user_location"], "link": row["url"],  \
#    "user_geo": list(map(float, row["user_geo"].strip("()").split(","))), \
#    "toxicity": row["toxicity"], "subjectivity": row["subjectivity"]} \
#    for index, row in tweets.iterrows()]

#data = tweets['data'].values.tolist()

# Index and add data to Solr with core 'toxictweets'
solr = pysolr.Solr("http://localhost:8983/solr/t", always_commit=True)
#print("Add data to Solr:")
# print(solr.add(tweets))

# Test indexed data
#query = "quarantine"
#query_search = "text: %s" % (query)
#fl_search = "id,text"

# search_results = solr.search(query_search, **{
#    'fl': fl_search
# }, rows=15)

# for result in search_results:
#    print(result["id"], result["text"])
query = "covid"
query_search = "text: %s" % (query)
results = solr.search(query_search, rows=15)

# The ``Results`` object stores total results found, by default the top
# ten most relevant results and any additional data like
# facets/highlighting/spelling/etc.
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print("'{0}'".format(result['text']))
