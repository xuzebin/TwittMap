#!/usr/bin/env python

from . import tweet_streamer
from tweet_callback import TweetCallback

import threading

class TweetStreamThread:

    def __init__(self, callback):
        self.callback = callback

    def stream_thread(self):
        tweet_streamer.register_callback(self.callback)
        tweet_streamer.start_stream()

    def start_thread(self):
        print 'thread started'
        # Create a thread for tweets streaming
        t = threading.Thread(target=self.stream_thread);
        t.setDaemon(True)
        t.start()


