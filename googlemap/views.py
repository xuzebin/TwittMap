from django.shortcuts import render
from django.http import HttpResponse

from . import tweet_streamer

import time
import json

from elasticsearch.elasticsearch_wrapper import ElasticsearchWrapper

es = ElasticsearchWrapper()

def index(request):
    return render(request, 'googlemap/index.html')

def first_fetch(request):
    print 'first_fetch'
    response = es.fetch_latest(1000)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')


def update_tweets(request):
    print 'update_tweets'
    response = es.fetch_latest(10)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')

def stop_tweets(request):
    print 'stop_tweets'
#    tweet_streamer.stop_stream()# stop the stream
    return HttpResponse()

def search(request):
    print 'search request'
    keyword = request.POST['keyword']
    response = es.search(keyword)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')

def geosearch(request):
    print 'geosearch request'
    location = request.POST.get('location')
    distance = request.POST.get('distance')
    print 'location: %s, radius: %s' % (location, distance)

    response = es.geosearch(location, distance, 2000)# search at most 2000 tweets
    print 'geosearch response: %s' % response
    response = response['hits']['hits']
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')



