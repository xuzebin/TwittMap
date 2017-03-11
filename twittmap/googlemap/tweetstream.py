#!/usr/bin/env python

import time
from getpass import getpass
from textwrap import TextWrapper
from datetime import datetime
import tweepy

import json

from tweetsobserver import TweetsObserver

consumer_key = 'wxKA6I6SNsedU9MIq35GGafN4';
consumer_secret = 'Nbuc9cHgI3UlTnVGGGaYGEWsbxoziYOrhnXIo5dnBhphurj4Fw';
access_token = '770112962380042241-txAffaFd4o4NMp9B94WWmZ4CV7HyvhY';
access_token_secret = 'KQ5s9uPWarXmivPZVOOW8HUXNjHhEm4oMqDnjdw4enSlJ';

observer = TweetsObserver()
TIMEZONE_OFFSET = datetime.utcnow() - datetime.now()

class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            coords = status.coordinates["coordinates"]
            if coords is not None:
                local_created_time = status.created_at - TIMEZONE_OFFSET;
                tweet = {
                    'name': status.author.screen_name,
                    'time': local_created_time.strftime("%Y/%m/%d %H:%M:%S"),
                    'location': {'lat': coords[1], 'lon': coords[0]},
                    'text': status.text
                }
                observer.flush_tweet(tweet)
                return True

        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'
        


def register_callback(callback):
    observer.register_callback(callback)

def start_stream():


    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    global stream
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)
    stream.filter(locations=[-180, -90, 180, 90])

def stop_stream():
    print 'stopping stream'
    observer.save_tweets()
    global stream
    stream.disconnect()



