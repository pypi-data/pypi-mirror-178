import requests

class TopicLandClient(object):

    def __init__(self, server) -> None:
        self.server = server

    def get_topics_names(self):
        url = "{}/api/topics".format(self.server)
        response = requests.get(url)
        return response.json()["topics"]
