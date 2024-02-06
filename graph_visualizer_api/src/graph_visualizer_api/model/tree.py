from .node import Node
from .edge import Edge
from .exceptions import GraphError
from typing import Optional


class TreeNode:
    """Model of a node in a tree.

    Represents a node in a tree structure.

    Attributes:
        node: Reference to the original graph node.
        all_children: List of all children nodes in the tree hierarchy.
    """

    def __init__(self, node: Node):
        self.node = node
        self.all_children = []

    def add_child(self, child_node: 'TreeNode') -> None:
        """Add a child node to the current node.

        :param child_node: Child node to add.
        """
        self.all_children.append(child_node)


class Tree:
    """Model of a tree.

    Tree class containing a list of tree nodes.

    Attributes:
        root: The root node of the tree.
        directed: Behaviour of the graph/tree.
    """

    def __init__(self, root_node: Node, directed: bool):
        self.root = TreeNode(root_node)
        self.directed = directed

    def update_tree(self, focused_node: Node, graph_edges: list[Edge]) -> None:
        """Update the tree based on the focused node in the graph.

        :param focused_node: The focused node in the graph.
        :param graph_edges: List of edges in the graph.
        """
        self.root = self._build_tree(focused_node, graph_edges, set())

    def _build_tree(self, current_node: Node, graph_edges: list[Edge], visited_nodes: set) -> Optional[TreeNode]:
        """Recursively build the tree starting from the current node.

        :param current_node: The current node.
        :param graph_edges: List of edges in the graph.
        :param visited_nodes: Set of visited nodes to handle cyclic graphs.
        :returns: The TreeNode representing the current node and its children.
        """
        if current_node in visited_nodes:
            return None

        tree_node = TreeNode(current_node)
        visited_nodes.add(current_node)

        if self.directed:
            children_edges = [edge for edge in graph_edges if edge.source == current_node]
        else:
            children_edges = [edge for edge in graph_edges if current_node in (edge.source, edge.target)]

        for child_edge in children_edges:
            if current_node == child_edge.source:
                child_node = child_edge.target
            else:
                child_node = child_edge.source
            child_tree_node = self._build_tree(child_node, graph_edges, visited_nodes)
            if child_tree_node:
                tree_node.add_child(child_tree_node)

        visited_nodes.remove(current_node)
        return tree_node
