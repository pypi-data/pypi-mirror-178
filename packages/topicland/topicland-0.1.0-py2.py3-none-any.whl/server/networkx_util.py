from sqlalchemy import text
from sqlalchemy import create_engine
import networkx as nx


class NetworkxUtil(object):

    def __init__(self, db_engine, topic: str) -> None:
        self.engine = db_engine
        self.topic = topic

        self.directed_graph: nx.DiGraph = None
        self.nondirected_graph: nx.Graph = None
        self.build_graph()

    def build_graph(self) -> nx.DiGraph:
        conn = self.engine.connect()

        self.directed_graph = nx.DiGraph()
        self.nondirected_graph = nx.Graph()

        sql = "SELECT name FROM characters WHERE topic='{}'".format(self.topic)
        result = conn.execute(text(sql))
        for row in result.all():
            self.directed_graph.add_node(row[0])
            self.nondirected_graph.add_node(row[0])

        sql = "SELECT source, target FROM relations WHERE topic='{}'".format(
            self.topic)
        result = conn.execute(text(sql))
        for row in result.all():
            self.directed_graph.add_edge(row[0], row[1])
            self.nondirected_graph.add_edge(row[0], row[1])

    def get_all_path(self, source, target, cutoff: int = -1, only_directed: bool = False):
        if only_directed:
            graph = self.directed_graph
        else:
            graph = self.nondirected_graph

        if cutoff > 0:
            return list(nx.all_simple_paths(graph, source, target, cutoff=cutoff))
        else:
            return list(nx.all_simple_paths(graph, source, target))

    def update_characters_weight(self) -> None:
        conn = self.engine.connect()

        page_rank_map = nx.pagerank(self.directed_graph)

        for name, rank_value in page_rank_map.items():
            sql = "UPDATE characters SET weight = {} WHERE topic='{}' AND name = '{}';".format(
                rank_value, self.topic, name)
            conn.execute(text(sql))

        conn.commit()

