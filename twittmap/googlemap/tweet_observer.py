#!/usr/bin/env python

class TweetObserver:
    def __init__(self):
        self.callback = None

    def register_callback(self, callback):
        self.callback = callback

    def flush_tweet(self, tweet):
        self.callback.notify(tweet)
    
    def save_tweets(self):
        self.callback.save_tweets()


