from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

from . import tweetstream

import Queue
import time
import threading
import json

from elasticsearch import ElasticsearchWrapper

class TweetCallback():
    def __init__(self, elasticsearch, collect_freq):
        self.id = 1
        self.tweet_list = []
        self.elasticsearch = elasticsearch
        self.collect_freq = collect_freq

    def notify(self, tweet):
        print len(self.tweet_list)
        self.tweet_list.append(tweet)

        if len(self.tweet_list) == self.collect_freq:
            self.save_tweets()

    def clear_tweets(self):
        print 'clearing tweets'
        del self.tweet_list[:]

    def save_tweets(self):
        print 'saving tweets'
        data = ''
        for tweet in self.tweet_list:
            data += '{"index": {"_id": "%s"}}\n' % self.id
            data += json.dumps(tweet) + '\n'
            self.id += 1
        print data
        response = self.elasticsearch.upload(data)
        print response
        
        self.clear_tweets()
        self.tweet_list = []
        


es = ElasticsearchWrapper('localhost:9200', 'twitter', 'tweet')
cb = TweetCallback(es, 20) # Upload to elasticsearch database every 20 tweets

def index(request):
    # Create a thread for tweets streaming
    t = threading.Thread(target=tweetstream_thread);
    t.setDaemon(True)
    t.start()

    return render(request, 'googlemap/index.html')

def update_tweets(request):
    response = json.dumps(cb.tweet_list)
    cb.clear_tweets()
    return HttpResponse(response, content_type='application/json')

def stop_tweets(request):
    tweetstream.stop_stream()# stop the stream
    return HttpResponse()

def search(request):
    keyword = request.POST['keyword']
    response = es.search(keyword)
    response = response['hits']['hits']
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')

def tweetstream_thread():
    tweetstream.register_callback(cb)
    tweetstream.start_stream()

