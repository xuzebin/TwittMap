from django.shortcuts import render
from django.http import HttpResponse

from . import tweet_streamer

import time
import json

from elasticsearch_wrapper import ElasticsearchWrapper
from tweet_callback import TweetCallback
from tweet_stream_thread import TweetStreamThread

es = ElasticsearchWrapper('localhost:9200', 'twitter', 'tweet')
callback = TweetCallback(es, 20) # Upload to elasticsearch database every 20 tweets

stream_thread = TweetStreamThread(callback)
stream_thread.start_thread()

# def tweetstream_thread():
#     tweetstream.register_callback(cb)
#     tweetstream.start_stream()


def index(request):
    return render(request, 'googlemap/index.html')

def update_tweets(request):
    response = es.fetch_latest(10)
    response = response['hits']['hits']
    response = json.dumps(response)
    print response
    return HttpResponse(response, content_type='application/json')

def stop_tweets(request):
    tweet_streamer.stop_stream()# stop the stream
    return HttpResponse()

def search(request):
    keyword = request.POST['keyword']
    response = es.search(keyword)
    response = response['hits']['hits']
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')

def geosearch(request):
    location = request.POST.get('location')
    distance = request.POST.get('distance')
    print 'location: %s, radius: %s' % (location, distance)

    response = es.geosearch(location, distance)
    print response
    response = response['hits']['hits']
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')



