from graph_visualizer_api.model.tree import Tree
import json_data_source_plugin.main as json_main
import yaml
import json

from django.shortcuts import render


def get_tree():
    graph = json_main.get_graph()

    node = graph.get_random_node()
    tree = Tree(None).from_graph(graph, 150)

    yaml_data = tree.to_json()

    return yaml_data


def d3_visualization(request):
    # Sample JSON data
    get_tree()

    with open("graph_visualizer_platform\\src\\graph_visualizer_platform\\tree_view_data.json", 'r') as file:
        json_data = file.read()

    print(json_data)

    return render(request, 'visualization.html', {'json_data': json_data})
