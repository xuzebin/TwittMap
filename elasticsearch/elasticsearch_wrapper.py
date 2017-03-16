#!/usr/bin/env python
import json, requests

from ConfigParser import ConfigParser

class ElasticsearchWrapper:
    def __init__(self):
        config = ConfigParser()
        config.read("setup.cfg")

        self.end_point = config.get('Elasticsearch', 'end_point')
        self.index = config.get('Elasticsearch', 'index')
        self.mapping_type = config.get('Elasticsearch', 'mapping_type')        
        self.address = 'http://%s/%s/%s' % (self.end_point, self.index, self.mapping_type)

    def create_index(self):
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
        print data
        response = requests.put(self.address, data=json.dumps(data))
        return response.text

    def upload(self, data):
        print 'uploading to databse...'
        upload_address = '%s/_bulk' % (self.address)
        response = requests.put(upload_address, data=data)
        print 'upload success'
        return response

    def search(self, keyword):
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
        
    def fetch_latest(self, top_n):
        data = {
            "query": {
                "match_all": {}
            },
            "size": top_n,
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


