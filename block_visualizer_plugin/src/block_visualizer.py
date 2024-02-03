from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.visualizer import Visualizer
from jinja2 import Environment, FileSystemLoader
import os


class BlockVisualizer(Visualizer):
    def generate_template(self, graph: Graph) -> str:
        script_folder = os.path.dirname(os.path.abspath(__file__))

        template_env = Environment(loader=FileSystemLoader(os.path.join(script_folder, 'template')))
        template = template_env.get_template('block_visualizer_template.jinja2')

        html_template = template.render(nodes=graph.nodes)

        return html_template
