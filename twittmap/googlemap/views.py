from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

from . import tweetstream

import Queue
import time
import threading
import json

q = Queue.Queue(maxsize = 100)

# Create your views here.
def index(request):
    t = threading.Thread(target=collect_tweets, args=(), kwargs={})
    t.setDaemon(True)
    t.start()
    return render(request, 'googlemap/index.html')

def update_tweets(request):
    locs = list(q.queue)
    with q.mutex:
        q.queue.clear()
    response = json.dumps(locs)
    return HttpResponse(response, content_type='application/json')

def collect_tweets():
    cb = TweetCallback()
    tweetstream.register_callback(cb)
    tweetstream.filter()

def stop_tweets(request):
    tweetstream.stop_stream()# stop the stream
    return HttpResponse()


class TweetCallback():
    def notify(self, tweet):
        q.put(tweet)






