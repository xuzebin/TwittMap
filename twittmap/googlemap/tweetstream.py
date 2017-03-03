#!/usr/bin/env python

import time
from getpass import getpass
from textwrap import TextWrapper

import tweepy

import Queue

from tweetsobserver import TweetsObserver

q = Queue.Queue(maxsize=10)
observer = TweetsObserver()

class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')


    def on_status(self, status):
        try:
#            print self.status_wrapper.fill(status.text)
            print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
            coords = status.coordinates["coordinates"]
            if coords is not None:
                tweet = {'location': coords, 'name': status.author.screen_name, 'time': status.created_at.strftime("%T %D"), 'source': status.source, 'text': self.status_wrapper.fill(status.text)}
                if q.full():
                    q.get()
                else:
                    observer.flush_tweet(tweet)
                    q.put(tweet)
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

def filter():
    consumer_key = 'wxKA6I6SNsedU9MIq35GGafN4';
    consumer_secret = 'Nbuc9cHgI3UlTnVGGGaYGEWsbxoziYOrhnXIo5dnBhphurj4Fw';
    access_token = '770112962380042241-txAffaFd4o4NMp9B94WWmZ4CV7HyvhY';
    access_token_secret = 'KQ5s9uPWarXmivPZVOOW8HUXNjHhEm4oMqDnjdw4enSlJ';

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    global stream
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)    
    stream.filter(locations=[-180, -90, 180, 90])

def stop_stream():
    global stream
    stream.disconnect()

def stream_twitts():
    
    consumer_key = 'wxKA6I6SNsedU9MIq35GGafN4';
    consumer_secret = 'Nbuc9cHgI3UlTnVGGGaYGEWsbxoziYOrhnXIo5dnBhphurj4Fw';
    access_token = '770112962380042241-txAffaFd4o4NMp9B94WWmZ4CV7HyvhY';
    access_token_secret = 'KQ5s9uPWarXmivPZVOOW8HUXNjHhEm4oMqDnjdw4enSlJ';

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)

    mode = 'sample'

    if mode == 'sample':
        stream.sample()

    elif mode == 'filter':
        follow_list = raw_input('Users to follow (comma separated): ').strip()
        track_list = raw_input('Keywords to track (comma seperated): ').strip()
        if follow_list:
            follow_list = [u for u in follow_list.split(',')]
            userid_list = []
            username_list = []
            
            for user in follow_list:
                if user.isdigit():
                    userid_list.append(user)
                else:
                    username_list.append(user)
            
            for username in username_list:
                user = tweepy.API().get_user(username)
                userid_list.append(user.id)
            
            follow_list = userid_list
        else:
            follow_list = None
        if track_list:
            track_list = [k for k in track_list.split(',')]
        else:
            track_list = None
        print follow_list
        stream.filter(follow_list, track_list)

