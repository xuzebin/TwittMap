import time
import tweepy
import json

from getpass import getpass
from datetime import datetime
from ConfigParser import ConfigParser
from tweet_observer import TweetObserver


TIMEZONE_OFFSET = datetime.utcnow() - datetime.now()

class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, observer):
        tweepy.StreamListener.__init__(self)
        self.observer = observer
    
    def on_status(self, status):
        try:
            coords = status.coordinates["coordinates"]
            if coords is not None:
                local_created_time = status.created_at - TIMEZONE_OFFSET;
                tweet = {
                    'name': status.author.screen_name,
                    'time': local_created_time.strftime("%Y/%m/%d %H:%M:%S"),
                    'location': {'lat': coords[1], 'lon': coords[0]},
                    'text': status.text,
                    'profile_image_url': status.author.profile_image_url
                }
                self.observer.flush_tweet(tweet)
                return True

        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'TweetStreamListener: An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'TweetStreamListener: timeout...'

    def on_connect(self):
        print 'TweetStreamListener: connect...'

    def on_exception(self, exception):
        print 'TweetStreamListener: exception... %s' % exception

    def on_disconnect(self, notice):
        print 'TweetStreamListener: disconnect... %s' % notice

    def on_warning(self, notice):
        print 'TweetStreamListener: warning... %s' % notice


class TweetStreamer:

    def __init__(self):
        self.stream = None
        self.observer = TweetObserver()

    def register_callback(self, callback):
        self.observer.register_callback(callback)

    def start_stream(self):
        consumer_key, consumer_secret, access_token, access_token_secret = self._read_config('setup.cfg')

        auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.stream = tweepy.Stream(auth, TweetStreamListener(self.observer), timeout=None)
        self.stream.filter(locations=[-180, -90, 180, 90])

    def stop_stream(self):
        print 'stopping stream...'
        self.observer.save_tweets()
        self.stream.disconnect()

    def _read_config(self, config_file):
        config = ConfigParser()
        config.read(config_file)

        consumer_key = config.get('TweetStreaming', 'consumer_key')
        consumer_secret = config.get('TweetStreaming', 'consumer_secret')
        access_token = config.get('TweetStreaming', 'access_token')
        access_token_secret = config.get('TweetStreaming', 'access_token_secret')

        return (consumer_key, consumer_secret, access_token, access_token_secret)


