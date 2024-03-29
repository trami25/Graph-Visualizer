import json

from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.visualizer import Visualizer
from jinja2 import Environment, FileSystemLoader
import os


class BlockVisualizer(Visualizer):
    def generate_template(self, graph: Graph) -> str:
        script_folder = os.path.dirname(os.path.abspath(__file__))

        template_env = Environment(loader=FileSystemLoader(os.path.join(script_folder, '../template')))
        template = template_env.get_template('block_visualizer_template.jinja2')

        nodes_json = [{'node_id': node.node_id, 'data': node.data} for node in graph.nodes]
        edges_json = [{'source': edge.source.node_id, 'target': edge.target.node_id, 'data': edge.data}
                                 for edge in graph.edges]
        directed_json = json.dumps(graph.directed)
        html_template = template.render(nodes_json=nodes_json, edges_json=edges_json, directed=directed_json)

        return html_template
