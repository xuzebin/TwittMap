#!/usr/bin/env python
import os
import sys
import threading

from twitter.tweet_streamer import TweetStreamer
from twitter.tweet_handler import TweetHandler
from elasticsearch.elasticsearch_wrapper import ElasticsearchWrapper

def start_streaming():
    es = ElasticsearchWrapper()
    streamer = TweetStreamer()
    streamer.set_handler(TweetHandler(es, collect_freq=5))
    streamer.start_stream()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittmap.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    """
    Run a separate thread for tweets streaming and uploading to elasticsearch
    """
    t = threading.Thread(target=start_streaming)
    t.setDaemon(True)
    t.start()

    execute_from_command_line(sys.argv)
    
