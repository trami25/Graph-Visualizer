from django.shortcuts import render
from django.http import HttpResponse
from simple_visualizer_plugin.simple_visualizer import SimpleVisualizer
from html_data_source_plugin.datasource import HtmlDataSource


# Create your views here.
def index(request):
    simple_visualizer = SimpleVisualizer()
    json_data_source = HtmlDataSource(node_cap=10)

    graph = json_data_source.generate_graph()
    return HttpResponse(simple_visualizer.generate_template(graph))
