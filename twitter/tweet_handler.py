from elasticsearch_wrapper import ElasticsearchWrapper

import json

class TweetHandler():
    """
    Handler for streaming tweets
    """
    def __init__(self, elasticsearch, collect_freq):
        """
        Args:
            elasticsearch: the instance of ElasticsearchWrapper
            collect_freq: frequency that decides tweets uploading to elasticsearch every [collect_freq]
        Returns: 
            None
        """
        self.id = 1
        self.tweet_list = []
        self.elasticsearch = elasticsearch
        self.collect_freq = collect_freq

    def on_tweet(self, tweet):
        """
        Handle the coming tweet from twitter streaming API
        Args:
            tweet: the formatted tweet data
        Returns:
            None
        """
        self.tweet_list.append(tweet)
        print len(self.tweet_list)
        if len(self.tweet_list) == self.collect_freq:
            self.save_tweets()

    def clear_tweets(self):
         print '[%s] clearing tweets...' % (self.__class__.__name__)
         del self.tweet_list[:]

    def save_tweets(self):
        print '[%s] saving tweets...' % (self.__class__.__name__)
        data = ''
        for tweet in self.tweet_list:
            data += '{"index": {"_id": "%s"}}\n' % self.id
            data += json.dumps(tweet) + '\n'
            self.id += 1
            print 'id: %s' % self.id

        # Upload tweets to elasticsearch
        response = self.elasticsearch.upload(data)
        print '[%s] elasticsearch response: %s' % (self.__class__.__name__, response)
        
        self.clear_tweets()
        self.tweet_list = []
        
