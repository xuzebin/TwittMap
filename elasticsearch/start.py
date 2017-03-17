#!/usr/bin/env python
# Upload streaming data to elasticsearch database

from elasticsearch_wrapper import ElasticsearchWrapper
from twitter.tweet_handler import TweetHandler
from twitter.tweet_streamer import TweetStreamer

if __name__ == "__main__":
    es = ElasticsearchWrapper()

    streamer = TweetStreamer()
    streamer.set_handler(TweetHandler(es, collect_freq=5))
    streamer.start_stream()
    

