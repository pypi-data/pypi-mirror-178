import model
import graphviz

def build_graph(graph: model.Graph) -> None:
    g_graph = graphviz.Digraph()

    # Add nodes

    for node in graph.nodes:
        g_graph.node(node.name, node.display_name, color='white', shape="circle",
        imagescale="true", fixedsize="true", style="filled",
        image="/Users/tobe/code/GraphBook/images/cyberpunk_edgerunner/{}.png".format(node.name))
    """
    for node in graph.nodes:
        g_graph.node(node.name, node.display_name, color='white', shape="circle",
        imagescale="true", fixedsize="true", style="filled")
    """

    # Add edges
    for edge in graph.edges:
        g_graph.edge(edge.source, edge.target, edge.relation)

    # Display graph
    g_graph.view()

def main() -> None:
    graph = model.Graph()
    db_config = model.DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph.load_from_db(db_config)
    build_graph(graph)

if __name__ == "__main__":
    main()
