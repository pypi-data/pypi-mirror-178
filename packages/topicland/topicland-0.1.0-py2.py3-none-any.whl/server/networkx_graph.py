import model
import networkx as nx
import matplotlib.pyplot as plt

def build_graph(graph: model.Graph) -> None:

    n_graph = nx.DiGraph() 

    # Add nodes
    for node in graph.nodes:
        n_graph.add_node(node.name)

    # Add edges
    for edge in graph.edges:
        n_graph.add_edge(edge.source, edge.target)

    # Display graph
    nx.draw_networkx(n_graph)

    # Notwork for Chinese
    #formatted_edge_labels = {(edge.source, edge.target): edge.relation for edge in graph.edges}
    #pos = nx.spring_layout(n_graph)
    #nx.draw_networkx_edge_labels(n_graph, pos, edge_labels=formatted_edge_labels)

    plt.show()

def main() -> None:
    graph = model.Graph()
    db_config = model.DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph.load_from_db(db_config)
    build_graph(graph)

if __name__ == "__main__":
    main()