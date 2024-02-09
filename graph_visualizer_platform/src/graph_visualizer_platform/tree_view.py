from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.tree import Tree
import json_data_source_plugin.main as json_main
import yaml
import json
from graph_visualizer_api.visualizer import Visualizer
from django.template.loader import get_template

from django.shortcuts import render


def get_tree(graph: Graph, node_id:int = None):

    if(node_id):
        node_id = 150
    tree = Tree(None).from_graph(graph, node_id)

    if(tree):
        yaml_data = tree.to_json()

    with open("graph_visualizer_platform\\src\\graph_visualizer_platform\\tree_view_data.json", 'r') as file:
        json_data = json.load(file)
    return json_data



def generate_template(graph: Graph, node_id: int = None) -> str:
    json_data = get_tree(graph, node_id)
    template = get_template("C:\\Users\\Aleksa\\Desktop\\Graph-Visualizer\\graph_visualizer_platform\\src\\visualization.html")
    json_data_str = json.dumps(json_data)
    html_template = template.render({'my_json_data': json_data_str})

    return html_template
