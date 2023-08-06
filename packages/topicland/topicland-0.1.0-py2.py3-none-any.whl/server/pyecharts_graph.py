import model
from pyecharts import options as opts
from pyecharts import charts


def build_graph(graph: model.Graph) -> None:

    # Add nodes
    nodes = []
    for node in graph.nodes:
        nodes.append({"name": node.name, "symbolSize": node.weight * 300})

    # Add edges
    links = []
    for edge in graph.edges:
        links.append({"source": edge.source, "target": edge.target})

    c = (
        charts.Graph()
        .add("", nodes, links, repulsion=8000)
        .set_global_opts(title_opts=opts.TitleOpts(title="Graph"))
        .render("pyecharts_graph.html")
    )

def main() -> None:
    graph = model.Graph()
    db_config = model.DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph.load_from_db(db_config)
    build_graph(graph)

if __name__ == "__main__":
    main()