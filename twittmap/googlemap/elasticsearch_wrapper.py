#!/usr/bin/env python
import json, requests

class ElasticsearchWrapper:
    def __init__(self, url, index, mapping_name):
        self.url = url
        self.index = index
        self.mapping_name = mapping_name
        self.address = 'http://%s/%s/%s' % (url, index, mapping_name)

    def create_index(self, index):
        data = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            },
            "mappings": {
                mapping_name: {
                    "properties": {
                        "name": { "type" : "text" },
                        "time": { "type": "date", "format": "yyyy/MM/dd HH:mm:ss"},
                        "location": { "type": "geo_point"},
                        "text": { "type": "text"}
                    }
                }
            }
        }
        response = requests.put(self.address, data=json.dumps(data))
        return response.text

    def upload(self, data):
        print 'uploading to databse...'
        upload_address = '%s/_bulk' % (self.address)
        response = requests.put(upload_address, data=data)
        return response

    def search(self, keyword):
        data = {
            "query": {
                "query_string": { "query": keyword }
            }
        }
        search_address = '%s/_search' % (self.address)
        response = requests.post(search_address, data=json.dumps(data))
        return response.json()

    def geosearch(self, location, distance):
        data = {
            "size":100,
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
