from . import tweet_streamer
from tweet_callback import TweetCallback

class TweetStreamThread:

    def __init__(self, callback):
        self.callback = callback

    def start_streaming(self):
        print 'start streaming'
        tweet_streamer.register_callback(self.callback)
        tweet_streamer.start_stream()
        

