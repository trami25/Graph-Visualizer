import os

from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.tree import Tree
import json_data_source_plugin.main as json_main
import yaml
import json
from graph_visualizer_api.visualizer import Visualizer
from django.template.loader import get_template

from django.shortcuts import render


def get_tree(graph: Graph, node_id: int = None):
    if not node_id or len(graph.nodes)==0:
        return {}

    tree = Tree(node_id).from_graph(graph, node_id)

    if (tree):
        yaml_data = tree.to_json()

    with open(os.path.join("graph_visualizer_platform", "src", "graph_visualizer_platform", "tree_view_data.json"),
              'r') as file:
        json_data = json.load(file)
    return json_data


def generate_template(graph: Graph, node_id: int = None) -> str:
    json_data = get_tree(graph, node_id)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = "visualizer/visualization.html"
    template = get_template(template_path)
    json_data_str = json.dumps(json_data)
    html_template = template.render({'my_json_data': json_data_str})

    return html_template
