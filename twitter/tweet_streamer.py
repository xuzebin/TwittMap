import time
import tweepy
import json

from getpass import getpass
from datetime import datetime
from ConfigParser import ConfigParser

class TweetStreamListener(tweepy.StreamListener):
    """
    Listener for streaming tweets.
    """
    def __init__(self, tweet_handler):
        """
        Args:
            tweet_handler: handler for tweets
        Returns:
            None
        """
        tweepy.StreamListener.__init__(self)
        self.tweet_handler = tweet_handler
        self.TIMEZONE_OFFSET = datetime.utcnow() - datetime.now()

    def on_status(self, status):
        """
        Callback when a new status arrived.
        Can be used for retrieving tweets
        """
        try:
            coords = status.coordinates["coordinates"]
            if coords is not None:
                local_created_time = status.created_at - self.TIMEZONE_OFFSET;
                tweet = {
                    'name': status.author.screen_name,
                    'time': local_created_time.strftime("%Y/%m/%d %H:%M:%S"),
                    'location': {'lat': coords[1], 'lon': coords[0]},
                    'text': status.text,
                    'profile_image_url': status.author.profile_image_url
                }
                self.tweet_handler.on_tweet(tweet)
                return True

        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'TweetStreamListener: An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print '[%s] timeout...' % (self.__class__.__name__)

    def on_connect(self):
        print '[%s] connect...' % (self.__class__.__name__)

    def on_exception(self, exception):
        print '[%s] exception... %s' % (self.__class__.__name__, exception)

    def on_disconnect(self, notice):
        print '[%s] disconnect... %s' % (self.__class__.__name__, notice)

    def on_warning(self, notice):
        print '[%s] warning... %s' % (self.__class__.__name__, notice)


class TweetStreamer:
    """
    Controller for tweets streaming
    """
    def __init__(self):
        self.stream = None
        self.tweet_handler = None

    def set_handler(self, handler):
        self.tweet_handler = handler

    def start_stream(self):
        """Start tweets streaming"""
        print '[%s] starting stream...' % (self.__class__.__name__)
        consumer_key, consumer_secret, access_token, access_token_secret = self._read_config('setup.cfg')

        auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        if self.tweet_handler is None:
            raise TypeError("tweet_handler not set!")

        self.stream = tweepy.Stream(auth, TweetStreamListener(self.tweet_handler), timeout=None)
        self.stream.filter(locations=[-180, -90, 180, 90])

    def stop_stream(self):
        """Stop streaming tweets"""
        print '[%s] stopping stream...' % (self.__class__.__name__)
        if tweet_handler is not None:
            self.tweet_handler.save_tweets()
        self.stream.disconnect()

    def _read_config(self, config_file):
        """
        Read from setup configuration file to set up twitter streaming.
        Args:
            config_file: the configuration file name
        Returns:
            A tuple containing the credentials for setting up tweets streaming.
        """
        config = ConfigParser()
        config.read(config_file)

        consumer_key = config.get('TweetStreaming', 'consumer_key')
        consumer_secret = config.get('TweetStreaming', 'consumer_secret')
        access_token = config.get('TweetStreaming', 'access_token')
        access_token_secret = config.get('TweetStreaming', 'access_token_secret')

        return (consumer_key, consumer_secret, access_token, access_token_secret)


