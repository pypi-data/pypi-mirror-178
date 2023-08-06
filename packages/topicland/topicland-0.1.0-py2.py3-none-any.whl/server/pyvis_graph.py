from pyvis.network import Network
import model

def build_graph(graph: model.Graph) -> None:

    net = Network()

    # Add nodes
    for node in graph.nodes:
        net.add_node(node.name)

    # Add edges
    for edge in graph.edges:
        net.add_edge(edge.source, edge.target)

    net.toggle_physics(True)
    net.show_buttons(filter_=['physics'])

    net.show('pyvis_graph.html')

def main() -> None:
    graph = model.Graph()
    db_config = model.DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph.load_from_db(db_config)
    build_graph(graph)

if __name__ == "__main__":
    main()