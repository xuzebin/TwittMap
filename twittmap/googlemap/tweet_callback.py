#!/usr/bin/env python

class TweetCallback():
    def __init__(self, elasticsearch, collect_freq):
        self.id = 1
        self.tweet_list = []
        self.elasticsearch = elasticsearch
        self.collect_freq = collect_freq

    def notify(self, tweet):
        self.tweet_list.append(tweet)

        if len(self.tweet_list) == self.collect_freq:
            self.save_tweets()

    def clear_tweets(self):
         print 'clearing tweets...'
         del self.tweet_list[:]

    def save_tweets(self):
        print 'saving tweets...'
        data = ''
        for tweet in self.tweet_list:
            data += '{"index": {"_id": "%s"}}\n' % self.id
            data += json.dumps(tweet) + '\n'
            self.id += 1
            print 'id: %s' % self.id

        print data
        # Upload tweets to elasticsearch
        response = self.elasticsearch.upload(data)
        print response
        
        self.clear_tweets()
        self.tweet_list = []
        
