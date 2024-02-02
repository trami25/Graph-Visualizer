from django.shortcuts import render
from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.visualizer import Visualizer


class SimpleViewVisualizer(Visualizer):
    def generate_template(self, graph: Graph) -> str:
        template_path = 'simple_view_visualizer_plugin/simple_view.html'
        context = {'graph_data': graph.nodes}
        return render(None, template_path, context).content.decode('utf-8')
