from array import array
import pymysql.cursors
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class DbConfig:
    host: str
    user: str
    password: str
    db: str

@dataclass
class Node:
    id: int
    name: str
    display_name: str = ""
    note: str = ""
    weight: float = 0.0
    #image: str = ""

@dataclass
class Edge:
    id: int
    source: int
    target: str
    relation: str = ""

@dataclass
class Group:
    id: int
    name: str
    node_name: str

class Graph:
    def __init__(self) -> None:
        self.nodes = []
        self.edges = []
        self.groups = []

    def __str__(self) -> str:
        return "Nodes: {},\nEdges: {},\nGroups: {}".format(self.nodes, self.edges, self.groups)

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    def add_group(self, group: Group) -> None:
        self.groups.append(group)
    
    def load_from_db(self, db_config: DbConfig, db: str) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            sql = "SELECT * FROM {}.nodes".format(db)
            cursor.execute(sql)
            result_set = cursor.fetchall()
            for item in result_set:
                node = Node(item["id"], item["name"], item["display_name"], item["note"], item["weight"])
                self.add_node(node)
                logging.info("Load node: {}".format(node))

            sql = "SELECT * FROM {}.edges".format(db)
            cursor.execute(sql)
            result_set = cursor.fetchall()
            for item in result_set:
                edge = Edge(item["id"], item["source"], item["target"], item["relation"])
                self.add_edge(edge)
                logging.info("Load edge: {}".format(edge))

            sql = "SELECT * FROM {}.teams".format(db)
            cursor.execute(sql)
            result_set = cursor.fetchall()
            for item in result_set:
                group = Group(item["id"], item["group_name"], item["node_name"])
                self.add_group(group)
                logging.info("Load group: {}".format(group))


def main():
    db_config = DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph = Graph()
    graph.load_from_db(db_config, "cyberpunk_edgerunner")
    print(graph)


if __name__ == "__main__":
    main()


