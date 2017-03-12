from django.shortcuts import render
from django.http import HttpResponse

from . import tweet_streamer

import time
import json

from elasticsearch_wrapper import ElasticsearchWrapper
from tweet_callback import TweetCallback
from tweet_stream_thread import TweetStreamThread

es = ElasticsearchWrapper()
#callback = TweetCallback(es, 20) # Upload to elasticsearch database every 20 tweets

# class TweetCallback():
#     def __init__(self, elasticsearch, collect_freq):
#         self.id = 1
#         self.tweet_list = []
#         self.elasticsearch = elasticsearch
#         self.collect_freq = collect_freq

#     def notify(self, tweet):
#         self.tweet_list.append(tweet)
#         print 'tweet_list len: %s' % len(self.tweet_list)
#         if len(self.tweet_list) == self.collect_freq:
#             self.save_tweets()

#     def clear_tweets(self):
#          print 'clearing tweets...'
#          del self.tweet_list[:]

#     def save_tweets(self):
#         print 'saving tweets...'
#         data = ''
#         for tweet in self.tweet_list:
#             data += '{"index": {"_id": "%s"}}\n' % self.id
#             data += json.dumps(tweet) + '\n'
#             self.id += 1
#             print 'id: %s' % self.id

#         # Upload tweets to elasticsearch
#         response = self.elasticsearch.upload(data)
#         print 'elasticsearch response: %s' % response
        
#         self.clear_tweets()
#         self.tweet_list = []



stream_thread = TweetStreamThread(TweetCallback(es, 10))
stream_thread.start_thread()

def index(request):
    return render(request, 'googlemap/index.html')

def update_tweets(request):
    print 'update_tweets'
    response = es.fetch_latest(10)
    response = response['hits']['hits']
    response = json.dumps(response)
    print 'fecth_latest %s' % response
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
    print 'geosearch response: %s' % response
    response = response['hits']['hits']
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')



