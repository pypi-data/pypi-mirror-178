#!/usr/bin/env python3

import sys
import configparser
import os
import logging

import db_service

def main():
    if len(sys.argv) <= 1:
        print("Need to pass the topicland ini config file")
    
    ini_config = configparser.ConfigParser()
    ini_config_path = sys.argv[1]
    ini_config.read(ini_config_path)

    db_config = db_service.DbConfig(ini_config["db"]["dbms"], ini_config["db"]["endpoint"],
                                ini_config["db"]["user"], ini_config["db"]["password"], ini_config["db"]["db_name"])
    service = db_service.DbService(db_config)

    # TODO: Only support to run in current directory
    official_topics_path = "../../Topics/"
    topic_name_list = [f for f in os.listdir(official_topics_path) if os.path.isdir(os.path.join(official_topics_path, f))]

    for topic_name in topic_name_list:
        logging.info("Try to import topic: {} in path: {}".format(topic_name, official_topics_path))
        service.import_topic(topic_name, official_topics_path)


    print("Finish importing official topics")



if __name__ == "__main__":
    main()