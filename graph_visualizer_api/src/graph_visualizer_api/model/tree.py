from .node import Node
from .edge import Edge
from .exceptions import GraphError
from typing import Optional

class TreeNode:
    """Model of a node in a tree.

    Represents a node in a tree structure.

    Attributes:
        node: Reference to the original graph node.
        children: List of children nodes in the tree.
    """

    def __init__(self, node: Node):
        self.node = node
        self.children = []

    def add_child(self, child_node: 'TreeNode') -> None:
        """Add a child node to the current node.

        :param child_node: Child node to add.
        """
        self.children.append(child_node)

class Tree:
    """Model of a tree.

    Tree class containing a list of tree nodes.

    Attributes:
        root: The root node of the tree.
    """

    def __init__(self, root_node: Node):
        self.root = TreeNode(root_node)

    def update_tree(self, focused_node: Node, graph_edges: list[Edge]) -> None:
        """Update the tree based on the focused node in the graph.

        :param focused_node: The focused node in the graph.
        :param graph_edges: List of edges in the graph.
        """
        self.root = self._build_tree(focused_node, graph_edges)

    def _build_tree(self, current_node: Node, graph_edges: list[Edge]) -> Optional[TreeNode]:
        """Recursively build the tree starting from the current node.

        :param current_node: The current node.
        :param graph_edges: List of edges in the graph.
        :returns: The TreeNode representing the current node and its children.
        """
        tree_node = TreeNode(current_node)
        children_edges = [edge for edge in graph_edges if edge.source == current_node]

        for child_edge in children_edges:
            child_node = child_edge.target
            child_tree_node = self._build_tree(child_node, graph_edges)
            if child_tree_node:
                tree_node.add_child(child_tree_node)

        return tree_node
