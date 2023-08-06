#!/usr/bin/env python3

import fire
from .topicland_client import TopicLandClient

class TopicLandCmd(object):

  def topic_list(self, server):
    client = TopicLandClient(server)
    return client.get_topics_names()

def main():
  fire.Fire(TopicLandCmd)

if __name__ == '__main__':
  main()

