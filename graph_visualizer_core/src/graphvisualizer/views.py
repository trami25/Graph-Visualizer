from django.shortcuts import render
from django.http import HttpResponse
from block_visualizer_plugin.block_visualizer import BlockVisualizer
from html_data_source_plugin.datasource import HtmlDataSource


# Create your views here.
def index(request):
    simple_visualizer = BlockVisualizer()
    json_data_source = HtmlDataSource()

    graph = json_data_source.generate_graph()
    return HttpResponse(simple_visualizer.generate_template(graph))
