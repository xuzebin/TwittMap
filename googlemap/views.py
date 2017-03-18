from django.shortcuts import render
from django.http import HttpResponse

import time
import json

from elasticsearch.elasticsearch_wrapper import ElasticsearchWrapper

es = ElasticsearchWrapper()

import threading

from twitter.tweet_streamer import TweetStreamer
from twitter.tweet_handler import TweetHandler

def start_streaming():
    es = ElasticsearchWrapper()
    streamer = TweetStreamer()
    streamer.set_handler(TweetHandler(es, collect_freq=5))
    streamer.start_stream()

"""
Run a separate thread for tweets streaming and uploading to elasticsearch
"""
t = threading.Thread(target=start_streaming)
t.setDaemon(True)
t.start()


def index(request):
    """
    Returns the page of twittmap
    """
    return render(request, 'googlemap/index.html')

def first_fetch(request):
    """
    Fetch 1000 tweets at the first request of twittmap or after reset.
    If there is no more than 1000 tweets in database, then returns as much as possbile.
    """
    print 'ajax request: first_fetch'
    response = es.fetch_latest(1000)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')


def update_tweets(request):
    """
    Fetch latest tweets from elasticsearch.
    Args: 
        request: Ajax request for fetching tweets
    Returns:
        10 latest tweets.
    """
    print 'ajax request: update_tweets'
    response = es.fetch_latest(10)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')

def stop_tweets(request):
    """
    Stop fetching tweets.
    Currently we won't stop streaming tweets
    """
    print 'ajax request: stop_tweets'
    return HttpResponse()

def search(request):
    """
    Search tweets by keyword
    Args:
        requst: Ajax request for searching tweets
    Returns:
        Tweets containing the keyword
    """
    print 'ajax request: search request'
    keyword = request.POST['keyword']
    response = es.search(keyword)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')

def geosearch(request):
    """
    Search tweets within a distance at a location
    Args:
        requst: Ajax request for geosearching tweets
    Returns:
        Tweets within the distance at the location
    """
    print 'ajax request: geosearch'
    location = request.POST.get('location')
    distance = request.POST.get('distance')
    print 'location: %s, radius: %s' % (location, distance)

    response = es.geosearch(location, distance, 2000)# search at most 2000 tweets
    print 'geosearch response: %s' % response

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')



