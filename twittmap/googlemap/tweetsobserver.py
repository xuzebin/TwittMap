#!/usr/bin/env python

class TweetsObserver:
    def __init__(self):
        self.__callback = None

    def register_callback(self, callback):
        self.__callback = callback

    def flush_tweet(self, tweet):
        self.__callback.notify(tweet)


