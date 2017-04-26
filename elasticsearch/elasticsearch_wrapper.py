import json, requests

from ConfigParser import ConfigParser

class ElasticsearchWrapper:
    """
    A wrapper for basic Elasticsearch operations.
    """
    def __init__(self):
        """
        Read from the setup configuration file to construct the elasticsearch URL.
        """
        config = ConfigParser()
        config.read("setup.cfg")

        self.end_point = config.get('Elasticsearch', 'end_point')
        self.index = config.get('Elasticsearch', 'index')
        self.mapping_type = config.get('Elasticsearch', 'mapping_type')        
        self.address = 'http://%s/%s/%s' % (self.end_point, self.index, self.mapping_type)

    def create_index(self):
        """
        Create the index for elasticsearch.
        Should be called and only called at the first time.
        """
        data = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            },
            "mappings": {
                self.mapping_type: {
                    "properties": {
                        "name": { "type" : "text" },
                        "time": { "type": "date", "format": "yyyy/MM/dd HH:mm:ss"},
                        "location": { "type": "geo_point"},
                        "text": { "type": "text"},
                        "profile_image_url": { "type": "text" }
                    }
                }
            }
        }
        response = requests.post(self.address, data=json.dumps(data))
        return response.text

    def upload(self, data):
        """
        Upload data to elasticsearch.
        Args:
            data: the json tweets data to upload
        Returns:
            Response for uploading.
        """
        upload_address = '%s/_bulk' % (self.address)
        response = requests.put(upload_address, data=data)
        return response

    def search(self, keyword):
        """
        Search tweets that contain the keyword.
        Args:
            keyword: the keyword to search
        Returns:
            Tweets containing the keyword in json format (Currently hardcoded restricted at most 2000 tweets)
        """
        data = {
            "size": 2000,
            "query": {
                "query_string": { "query": keyword }
            }
        }
        search_address = '%s/_search' % (self.address)
        response = requests.post(search_address, data=json.dumps(data))

        return response.json()

    def geosearch(self, location, distance, size):
        """
        Search tweets that locate within a distance of a location.
        Args:
            location: the center of the search scope
            distance: the radius of the the search scope
            size: the maximum size of tweets to be searched
        Returns:
            Tweets that are within the distance of a center.
        """
        data = {
            "size": size,
            "query": {
                "bool": {
                    "must": {
                        "match_all": {}
                    },
                    "filter": {
                        "geo_distance": {
                            "distance": '%skm' % (distance),
                            "location": location
                        }
                    }
                }
            }
        }
        search_address = '%s/_search' % (self.address)
        response = requests.post(search_address, data=json.dumps(data))
        return response.json()
        
    def fetch_latest(self, num):
        """
        Fetch latest tweets from elasticsearch based on the post date of the tweet.
        Args:
            num: the latest num number of tweets to fetch
        Returns:
            [num] number of latest Tweets.
        """
        data = {
            "query": {
                "match_all": {}
            },
            "size": num,
            "sort": [
                {
                    "time": {
                        "order": "desc"
                    }
                }
            ]
        }
        search_address = '%s/_search' % (self.address)
        response = requests.post(search_address, data=json.dumps(data))
        return response.json()


