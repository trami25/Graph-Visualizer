from jinja2 import Environment, FileSystemLoader
from graph_visualizer_api.visualizer import Visualizer
from graph_visualizer_api.model.graph import Graph


class SimpleVisualizer(Visualizer):
    def generate_template(self, graph: Graph) -> str:
        env = Environment(loader=FileSystemLoader("C:\\Users\\mniko\\PycharmProjects\\Graph-VisualizerSOK\\simple_visualizer_plugin\\template"))
        template = env.get_template("simple_visualizer_plugin/simple_visualizer_template.jinja2")

        html = template.render(graph=graph)

        return html
