#!/usr/bin/env python

from elasticsearch_wrapper import ElasticsearchWrapper
from twitter.tweet_handler import TweetHandler
from twitter.tweet_streamer import TweetStreamer

if __name__ == "__main__":
    """
    Start the process for fetching twitter streaming data and uploading to elasticsearch
    """
    es = ElasticsearchWrapper()

    streamer = TweetStreamer()
    streamer.set_handler(TweetHandler(es, collect_freq=5))
    streamer.start_stream()
    

