import os.path
from typing import List
from .graph import Graph
import yaml
import json

class TreeNode:
    """Model of a node in a tree."""

    def __init__(self, node_id, data):
        self.node_id = node_id
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class Tree:
    """Model of a tree."""

    def __init__(self, root):
        self.root = root

    def __str__(self):
        return self._tree_str(self.root)

    def _tree_str(self, node: TreeNode, level=0):
        result = "  " * level + f"Node[{node.node_id}]\n"
        for child in node.children:
            result += self._tree_str(child, level + 1)
        return result

    def from_graph(self, graph: Graph, start_node_id):
        """Construct a tree from a graph starting from the specified node."""
        start_node = graph.get_node_by_id(start_node_id)
        if start_node is None:
            return None

        visited = set()
        tree_node = self._dfs(graph, start_node, visited)

        if tree_node:
            return Tree(tree_node)
        else:
            return None

    def _dfs(self, graph: Graph, node: TreeNode, visited: List):
        """Depth-First Search traversal to construct the tree."""
        if node.node_id in visited:
            return None

        visited.add(node.node_id)
        tree_node = TreeNode(node.node_id, node.data)

        for neighbor in self._get_neighbors(graph, node):
            child_node = self._dfs(graph, neighbor, visited)
            if child_node:
                tree_node.add_child(child_node)

        return tree_node

    def _get_neighbors(self, graph, node):
        """Get neighboring nodes of a given node."""
        neighbors = []
        for edge in graph.edges:
            if edge.source == node:
                neighbors.append(edge.target)
            elif edge.target == node:
                neighbors.append(edge.source)
        return neighbors


    def to_yaml(self):
        """Convert the tree structure to YAML format."""
        yaml_data = self._tree_to_yaml(self.root)
        with open("graph_visualizer_platform\\src\\graph_visualizer_platform\\tree_view_data.yaml", "w") as file:
            for line in yaml_data:
                file.write(line + '\n')
            
        return yaml_data

    def _tree_to_yaml(self, node: TreeNode, indentation=""):
        """Convert the tree to YAML format."""
        yaml_data = []
        yaml_data.append(indentation + f"id: {node.node_id}")
        yaml_data.append(indentation + f"data: {node.data}")
        yaml_data.append(indentation + "children:")
        for child in reversed(node.children):
            child_yaml = self._tree_to_yaml(child, indentation + "  ")
            yaml_data.extend(child_yaml)
        return yaml_data


    def to_json(self):
        """Convert the tree structure to JSON format."""
        json_data = self._tree_to_json(self.root)
        with open(os.path.join("graph_visualizer_platform", "src", "graph_visualizer_platform", "tree_view_data.json"), "w") as file:
            json.dump(json_data, file, indent=4)
        return json_data

    def _tree_to_json(self, node: TreeNode):
        """Convert the tree to JSON format."""
        json_data = {
            "id": node.node_id,
            "data": node.data,
            "children": []
        }
        for child in node.children:
            child_json = self._tree_to_json(child)
            json_data["children"].append(child_json)
        return json_data