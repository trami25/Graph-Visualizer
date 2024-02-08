import json

from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.visualizer import Visualizer
from jinja2 import Environment, FileSystemLoader
import os

def default(obj):
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    else:
        raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))
class BlockVisualizer(Visualizer):
    def generate_template(self, graph: Graph) -> str:
        script_folder = os.path.dirname(os.path.abspath(__file__))

        template_env = Environment(loader=FileSystemLoader(os.path.join(script_folder, '../template')))
        template = template_env.get_template('block_visualizer_template.jinja2')

        nodes_json = json.dumps([{'node_id': node.node_id, 'data': node.data} for node in graph.nodes])
        edges_json = json.dumps([{'source': edge.source.node_id, 'target': edge.target.node_id, 'data': edge.data}
                                 for edge in graph.edges])

        html_template = template.render(nodes_json=nodes_json, edges_json=edges_json, directed = graph.directed)

        return html_template
