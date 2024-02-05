import os

from jinja2 import Environment, FileSystemLoader
from graph_visualizer_api.visualizer import Visualizer
from graph_visualizer_api.model.graph import Graph


class SimpleVisualizer(Visualizer):
    """Generates HTML template for visualizing a graph using Jinja2.

    This class is a plugin that implements the visualizer for the Graph Visualizer. It uses Jinja2 templates
    to generate HTML for visualizing a graph.

    Attributes:
        None
    """

    def generate_template(self, graph: Graph) -> str:
        """Generates HTML template for the given graph.

        :param graph: Graph to be visualized.
        :return: HTML template as a string.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "../template")

        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template("simple_visualizer_plugin/simple_visualizer_template.jinja2")

        html = template.render(graph=graph)

        return html
