import time
import requests
import json

def query_solr(query):
    start=time.time()
    print(query)
    json_data=query_multi_word(query)
    # if len(json_data["response"]["docs"]) == 1:
    #     if json_data["response"]["docs"]["text"] == ("No results"):
    #         json_data = query_spell_check(query)
    end=time.time()
    print("time elapse: ****{}".format(str(end-start)))
    return json_data


def query_index(query_url):
	""" Query index given formatted query to API """
	print(query_url)
	r = requests.get(query_url)
	r.raise_for_status()
	json_data = r.json() #dict type
	#print("QUESTY INDEX")
	if len(json_data["response"]["docs"])>0:

		# for text in json_data["response"]["docs"]:

		# 	if "_childDocuments_" in rest:
		# 		print("underscore!")
		# 		rest["childDocuments"]=rest["_childDocuments_"]
		# 		del rest["_childDocuments_"]
		return json_data
	else:
            query = '{"response": {"docs" : {"text":"No results"}}}'
            query = json.loads(query)

            return query 



def query_one_word(query): 
    
    #one word search

    """ to query reviews: Clean query and generate query string to post to API"""
	#query="\"AND\"".join(clean_review(query))
    #query="\"AND\"".join(query)
	#query_url= "http://127.0.0.1:8983/solr/food/query?q={!parent%20which=path:1.restaurants%20AND%20score=total}path:2.restaurants.reviews%20AND%20review_body:(\""+query+"\")&fl=*,[child%20parentFilter=path:1.restaurants%20childFilter=review_body:(\""+query+"\") limit=10]&sort=score%20desc"

    query_url =  "http://localhost:8983/solr/tweet/select?indent=true&q.op=OR&q=text%3A"+query

    # "http://localhost:8983/solr/tweet/select?indent=true&q.op=OR&q=text%3Acovid"

    return query_index(query_url)

def query_multi_word(query):

    query_list = query.split("+")
    query_url = "http://localhost:8983/solr/tweet/select?indent=true&q.op=OR&q=text%3A"
    if len(query_list) == 1:
        return query_one_word(query)
    else:
        query_url += "%22"
        for word in query_list:
            query_url += word + "%20"

        query_url = query_url[:-3]
        query_url += "%22"
        
        return query_index(query_url)



def query_spell_check(query):
     
    query_list = query.split("+")
    query_url = "http://localhost:8983/solr/tweet/spell?indent=true&q.op=OR&q=text%3A"
    if len(query_list) == 1:
        query_url += query_list[0]
        #print(query_url)
        r = requests.get(query_url)
        r.raise_for_status()
        json_data = r.json() #dict type
        #print(len(json_data["spellcheck"]["suggestions"]))

        if len(json_data["spellcheck"]["suggestions"])>0:
                        
            suggestions = json_data["spellcheck"]["suggestions"]
            spell_check_dict = {}
            length = len(suggestions)
            for i in range(int(length/2)):
                word = suggestions[2*i]
                suggestion = suggestions[2*i+1]['suggestion']
                suggestion_list = []
                num_of_suggestion = 4 if len(suggestion) > 5 else len(suggestion)
                for j in range(num_of_suggestion):
                    suggestion_list.append(suggestion[j]['word'])

                spell_check_dict[word] = suggestion_list
                #print(spell_check_dict)
                json_response = json.loads(json.dumps(spell_check_dict))
            
            
            print(json_response)
            return json_response
        else:
            json_response = '{}'
            json_response = json.loads(json_response)

        return json_response


    else:
        query_url += "%22"
        for word in query_list:
            query_url += word + "%20"

        query_url = query_url[:-3]
        query_url += "%22"

        r = requests.get(query_url)
        r.raise_for_status()
        json_data = r.json() #dict type
        if len(json_data["spellcheck"]["suggestions"])>0:
            #TODO: extract all the query suggestion words
            return json_data
        else:
            json_response = '{"spellcheck": {"suggestions" : {"text":"No results"}}}'
            json_response = json.loads(json_response)

        return json_response




def query_tweets_each_user():
    
    query_url = "http://localhost:8983/solr/tweet/select?facet.field=author_id&facet=true&indent=true&q.op=OR&q=*%3A*&rows=0"
    print(query_url)
    r = requests.get(query_url)
    r.raise_for_status()
    json_data = r.json() #dict type

    return json_data

def query_tweets_type():
    query_url = "http://localhost:8983/solr/tweet/select?facet.field=keyword&facet=true&indent=true&q.op=OR&q=*%3A*&rows=0"
    print(query_url)
    r = requests.get(query_url)
    r.raise_for_status()
    json_data = r.json() #dict type

    return json_data