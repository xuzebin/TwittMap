#!/usr/bin/env python
# Upload streaming data to elasticsearch database

from elasticsearch_wrapper import ElasticsearchWrapper
from twitter.tweet_callback import TweetCallback
from twitter.tweet_stream_thread import TweetStreamThread
from twitter.tweet_streamer import TweetStreamer

if __name__ == "__main__":
    es = ElasticsearchWrapper()

    streamer = TweetStreamer()
    streamer.register_callback(TweetCallback(es, collect_freq=5))
    streamer.start_stream()
    

