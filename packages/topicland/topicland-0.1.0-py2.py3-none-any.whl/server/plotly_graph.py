from dash import Dash, html
import dash_cytoscape as cyto
import model

def build_graph(graph: model.Graph) -> None:
    app = Dash(__name__)

    nodes = [{"data": {"id": node.name, "label": node.name}} for node in graph.nodes]
    edges = [{"data": {"source": edge.source, "target": edge.target}} for edge in graph.edges]
    elements = nodes + edges

    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            elements=elements,
            layout={'name': 'breadthfirst'},
            style={'width': '800px', 'height': '800px'}
        )
    ])

    app.run_server(debug=True)

def main() -> None:
    graph = model.Graph()
    db_config = model.DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph.load_from_db(db_config)
    build_graph(graph)

if __name__ == "__main__":
    main()