#!/usr/bin/env python

# Upload streaming data to elasticsearch database

#from elasticsearch.elasticsearch_wrapper import ElasticsearchWrapper
from elasticsearch_wrapper import ElasticsearchWrapper
from googlemap.tweet_callback import TweetCallback
from googlemap.tweet_stream_thread import TweetStreamThread

if __name__ == "__main__":
    es = ElasticsearchWrapper()
    stream_process = TweetStreamThread(TweetCallback(es, 5))
    stream_process.start_streaming()

