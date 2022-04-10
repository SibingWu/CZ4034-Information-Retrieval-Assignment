from django.shortcuts import render

from django.http import JsonResponse
from datetime import date
from matplotlib.pyplot import pie
import requests

from bar_plot import draw_count_bar_chart 
from pie_plot import draw_sentiment_pie_chart


from .query import *
# Create your views here.

def get_tweet(tweets):
	""" return rest and asso reviews """
	#for tweet in tweets:
		# if "childDocuments" in rest:
		# 	for rev in rest["childDocuments"]:
		# 		#print(rev["id"])
		# 		#print(Review.objects.get(id=rev["id"]).review_body)
		# 		rev["review_body"]=Review.objects.get(id=rev["id"]).review_body
	return tweets

def results(request):
	''' Result page '''
	# Your code
	if (request.method == 'GET') and ('search_box' in request.GET): # If the form is submitted

		query = request.GET.get('search_box', None)
		#print(query)
		results=query_solr(query)
		tweets=get_tweet(results["response"]["docs"])

		request.session['tweets'] = tweets
		request.session['query'] = query
		
		#print(len(tweets))
		if (len(tweets) < 20):
			print(len(tweets))
			json_data = query_spell_check(query)
			return render(request, 'filters.html', {'query': query, 'results':tweets, 'spellchecks':json_data})
        
		return render(request, 'filters.html', {'query': query, 'results':tweets})
	
	
		
	return JsonResponse({'hello': 'search box was empty'})

def check_filter(request):

	tweets = request.session['tweets']
	query = request.session['query'] 

	if (request.method == 'GET') and ('sentiment' in request.GET):
		
		option = request.GET["sentiment"]
		
		if (option == "all"):
			
			tweets = tweets
			
		elif (option == 'positive'):
			
			tweets = [tweet for tweet in tweets if tweet['sentiment'] == [4.0]]
			#print(tweets[0])
		elif (option == 'negative'):
			
			tweets = [tweet for tweet in tweets if tweet['sentiment'] == [0.0]]
		elif (option == 'neutral'):
			
			tweets = [tweet for tweet in tweets if tweet['sentiment'] == [2.0]]

		
		return render(request, 'filters.html',{'query': query, 'results': tweets, 'sentiment': option})



def tweets_each_user(request):

    if (request.method == 'GET') and ('TweetsByEachUser' in request.GET):

        results=query_tweets_each_user()
        tweets = get_tweet(results["facet_counts"]["facet_fields"]["author_id"])

        return render(request, 'tweetsByEachUser.html', {'results': tweets})
        
    return JsonResponse({'hello': 'empty'})

def home_button(request):
	''' Home View '''
	# Your code
	if (request.method == 'GET') and ('home' in request.GET):

		return render(request, 'homepage.html')

def home(request):
	return render(request, 'homepage.html')

def tweetsType(request):

    if (request.method == 'GET') and ('TweetsType' in request.GET):

        results=query_tweets_type()
        tweets = get_tweet(results["facet_counts"]["facet_fields"]["keyword"])

        return render(request, 'tweetsType.html', {'results': tweets})
        
    return JsonResponse({'hello': 'empty'})


def showCharts(request):

	query = request.session['query'] 

	if (request.method == 'GET') and ('charts' in request.GET):
		bar_results = query_bar_charts(query)
		pie_results = query_pie_charts(query)

		bar_chart = draw_count_bar_chart(bar_results)
		pie_chart = draw_sentiment_pie_chart(pie_results)

		return render(request, 'charts.html',{'bar_chart': bar_chart, 'pie_chart': pie_chart})
