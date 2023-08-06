#!/usr/bin/env python3

import os
import sys
import logging
import configparser
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import db_service

logger = logging.getLogger("topicland")

"""
Init flask web app.
"""
app = Flask(__name__,
            template_folder="./dist/",
            static_folder="./dist",
            static_url_path="")
cors = CORS(app, resources=r'/*')
app.config['CORS_HEADERS'] = 'Content-Type'

"""
Read config from ini config file.
"""
ini_config = configparser.ConfigParser()
ini_config_path = "./topicland.ini"
# Get config file from the first argument
if len(sys.argv) > 1:
    ini_config_path = sys.argv[1]
ini_config.read(ini_config_path)
# Get all config and print
all_config = dict(ini_config.items('server'))
all_config.update(dict(ini_config.items('db')))
print("Load init config file: {} and get all config: {}".format(
    ini_config_path, all_config))

"""
Init database service.
"""
db_config = db_service.DbConfig(ini_config["db"]["dbms"], ini_config["db"]["endpoint"],
                                ini_config["db"]["user"], ini_config["db"]["password"], ini_config["db"]["db_name"])
db_service = db_service.DbService(db_config)
db_service.init_database()
db_service.init_tables()

"""
Render the vue generated single page app.
"""
@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")


@app.route('/api/topics', methods=['GET', 'POST'])
@cross_origin()
def handle_topics():
    if request.method == "GET":
        result = {"topics": db_service.get_topics()}
        return jsonify(result)
    elif request.method == "POST":
        name = request.json["name"]
        db_service.create_topic(name)
        return jsonify({"code": 0})


@app.route('/api/topics_statistics', methods=['GET'])
@cross_origin()
def get_topics_statistics():
    if request.method == "GET":
        #tobedev
        if "count" in request.args:
            count = request.args.get("count", type=int)
            result = db_service.get_topics_statistics(count)
        elif "topic_name" in request.args:
            count = request.args.get("topic_name", type=str)
            result = db_service.get_one_topic_statistics(count)
        else:
            result = db_service.get_all_topics_statistics()
        return jsonify(result)


@app.route('/api/topics/<topic>', methods=['DELETE'])
@cross_origin()
def delete_topic(topic):
    if request.method == "DELETE":
        db_service.delete_topic(topic)
        return jsonify({"code": 0})


@app.route('/api/topics/<topic>/characters', methods=['GET', 'POST'])
@cross_origin()
def handle_characters(topic):
    if request.method == "GET":
        chosen_characters_names = request.args.getlist(
            'chosen_characters_names[]')
        result = {"characters": db_service.get_characters(
            topic, chosen_characters_names)}
        return jsonify(result)
    elif request.method == "POST":

        if "name" in request.json and "note" in request.json and "image_name" in request.json:
            name = request.json["name"]
            note = request.json["note"]
            image_name = request.json["image_name"]
            db_service.create_character(topic, name, note, image_name)
        elif "insert_characters" in request.json and "update_characters" in request.json and "delete_characters" in request.json:
            insert_characters = request.json["insert_characters"]
            update_characters = request.json["update_characters"]
            delete_characters = request.json["delete_characters"]
            db_service.update_characters(
                topic, insert_characters, update_characters, delete_characters)
        return jsonify({"code": 0})

@app.route('/api/topics/<topic>/export', methods=['POST'])
@cross_origin()
def handle_topic_export(topic):
    if request.method == "POST":
        path = request.json["path"]
        db_service.export_topic(topic, path)
        return jsonify({"code": 0})

@app.route('/api/topics/<topic>/import', methods=['POST'])
@cross_origin()
def handle_topic_import(topic):
    if request.method == "POST":
        path = request.json["path"]
        db_service.import_topic(topic, path)
        return jsonify({"code": 0})

@app.route('/api/topics/<topic>/characters/<character>', methods=['GET'])
@cross_origin()
def get_character(topic, character):
    if request.method == "GET":
        result = {
            "character": db_service.get_character(topic, character),
        }
        return jsonify(result)

@app.route('/api/topics/<topic>/characters/<character>/relations', methods=['GET'])
@cross_origin()
def get_character_relatioins(topic, character):
    if request.method == "GET":
        result = {
            "character": db_service.get_character(topic, character),
            "upstream_characters_and_relations": db_service.get_upstream_characters_and_relations(topic, character),
            "downstream_characters_and_relations": db_service.get_downstream_characters_and_relations(topic, character)
        }
        return jsonify(result)

@app.route('/api/topics/<topic>/characters_names', methods=['GET'])
@cross_origin()
def get_characters_names(topic):
    if request.method == "GET":
        chosen_groups = request.args.getlist('chosen_groups[]')
        result = {"characters_names": db_service.get_characters_names_in_groups(
            topic, chosen_groups)}
        return jsonify(result)


@app.route('/api/topics/<topic>/character_image', methods=['POST'])
@cross_origin()
def upload_character_image(topic):
    if request.method == "POST":
        IMAGES_DIR = "./dist/images/"
        TOPIC_IMAGES_DIR = "{}{}/".format(IMAGES_DIR, topic)

        # Create directory recursively if not exists
        if not os.path.exists(TOPIC_IMAGES_DIR):
            os.makedirs(TOPIC_IMAGES_DIR)

        # Save the image file
        file = request.files.get('file')
        file_name = file.filename
        file_path = "{}{}".format(TOPIC_IMAGES_DIR, file_name)

        if os.path.exists(file_path):
            logger.warning("Image file already exists, try to overwrite it")
        file.save(file_path)

        return jsonify({'code': 0})


@app.route('/api/topics/<topic>/relations', methods=['GET', 'POST'])
@cross_origin()
def handle_relations(topic):
    if request.method == "GET":
        result = {"relations": db_service.get_relations(topic)}
        return jsonify(result)

    elif request.method == "POST":
        if "source" in request.json and "target" in request.json and "relation" in request.json:
            source = request.json["source"]
            target = request.json["target"]
            relation = request.json["relation"]
            note = request.json["note"]
            db_service.create_relation(topic, source, target, relation, note)
        elif "character_name" in request.json and "upstream_relations" in request.json and "downstream_relations" in request.json:
            character_name = request.json["character_name"]
            upstream_relations = request.json["upstream_relations"]
            downstream_relations = request.json["downstream_relations"]
            db_service.add_relations_for_character(
                topic, character_name, upstream_relations, downstream_relations)
        elif "insert_relations" in request.json and "update_relations" in request.json and "delete_relations" in request.json:
            insert_relations = request.json["insert_relations"]
            update_relations = request.json["update_relations"]
            delete_relations = request.json["delete_relations"]
            db_service.update_relations(
                topic, insert_relations, update_relations, delete_relations)
        return jsonify({"code": 0})


@app.route('/api/topics/<topic>/groups', methods=['GET', 'POST'])
@cross_origin()
def handle_groups(topic):
    if request.method == "GET":
        result = {"groups": db_service.get_groups(topic)}
        return jsonify(result)
    elif request.method == "POST":
        if "group_name" in request.json and "character_name" in request.json:
            group_name = request.json["group_name"]
            character_name = request.json["character_name"]
            db_service.create_group(topic, group_name, character_name)
        elif "groups_names" in request.json and "character_name" in request.json:
            groups_names = request.json["groups_names"]
            character_name = request.json["character_name"]
            db_service.join_groups(topic, character_name, groups_names)
        elif "insert_groups" in request.json and "update_groups" in request.json and "delete_groups" in request.json:
            insert_groups = request.json["insert_groups"]
            update_groups = request.json["update_groups"]
            delete_groups = request.json["delete_groups"]
            db_service.update_groups(
                topic, insert_groups, update_groups, delete_groups)

        return jsonify({"code": 0})


@app.route('/api/topics/<topic>/groups_names', methods=['GET'])
@cross_origin()
def get_groups_names(topic):
    if request.method == "GET":
        result = {"groups_names": db_service.get_groups_names(topic)}
        return jsonify(result)

@app.route('/api/topics/<topic>/groups_characters', methods=['GET'])
@cross_origin()
def get_groups_and_characters(topic):
    if request.method == "GET":
        result = {"groups_and_characters": db_service.get_groups_and_characters(topic)}
        return jsonify(result)

@app.route('/api/topics/<topic>/paths', methods=['GET'])
@cross_origin()
def get_node_node_paths(topic):
    if request.method == "GET":
        source = request.args.get('source', type=str)
        target = request.args.get('target', type=str)
        cutoff = request.args.get('cutoff', default=-1, type=int)
        only_directed = request.args.get(
            'only_directed', default=False, type=lambda v: v.lower() == 'true')

        if source and target:
            paths = db_service.compute_paths(
                topic, source, target, cutoff, only_directed)
            result = {"paths": paths}
        else:
            # TODO: Throw error if failed
            result = {"code": -1}
        return jsonify(result)


@app.route('/api/topics/<topic>/weights', methods=['PUT'])
@cross_origin()
def update_characters_weights(topic):
    if request.method == "PUT":
        db_service.update_characters_weights(topic)
        result = {"code": 0}
        return jsonify(result)


def main():
  app.run(host=ini_config["server"]["host"],
          port=int(ini_config["server"]["port"]),
          threaded=True,
          debug=(ini_config["server"]["debug"].lower() == "true"))


if __name__ == "__main__":
  main()
