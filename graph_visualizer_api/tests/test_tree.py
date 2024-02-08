import unittest
from graph_visualizer_api.model.node import Node
from graph_visualizer_api.model.edge import Edge
from graph_visualizer_api.model.tree import Tree
from graph_visualizer_api.model.graph import Graph
import unittest
from typing import List


class TestTree(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(1, {})
        self.node2 = Node(2, {})
        self.node3 = Node(3, {})
        self.nodes = [self.node1, self.node2, self.node3]

    def test_update_tree_undirected(self):
        edges = [Edge(self.node1, self.node2, {}), Edge(self.node2, self.node3, {})]
        graph = Graph(self.nodes,edges)
        tree = Tree(None).from_graph(graph, self.node1.node_id)

        self.assertEqual(tree.root.node_id, self.node1.node_id)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].node_id, self.node2.node_id)
        self.assertEqual(len(tree.root.children[0].children), 1)
        self.assertEqual(tree.root.children[0].children[0].node_id, self.node3.node_id)
        self.assertEqual(len(tree.root.children[0].children[0].children), 0)

    def test_update_tree_directed(self):
        edges = [Edge(self.node1, self.node2, {}), Edge(self.node2, self.node3, {})]
        graph = Graph(self.nodes,edges)
        tree = Tree(None).from_graph(graph, self.node1.node_id)

        self.assertEqual(tree.root.node_id, self.node1.node_id)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].node_id, self.node2.node_id)
        self.assertEqual(len(tree.root.children[0].children), 1)
        self.assertEqual(tree.root.children[0].children[0].node_id, self.node3.node_id)
        self.assertEqual(len(tree.root.children[0].children[0].children), 0)

    def test_update_tree_mixed_undirected(self):
        edges = [Edge(self.node1, self.node2, {}), Edge(self.node2, self.node3, {}), Edge(self.node3, self.node1, {})]
        graph = Graph(self.nodes,edges)
        tree = Tree(None).from_graph(graph, self.node1.node_id)

        self.assertEqual(tree.root.node_id, self.node1.node_id)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].node_id, self.node2.node_id)
        self.assertEqual(len(tree.root.children[0].children), 1)

    def test_update_tree_mixed_directed(self):
        edges = [Edge(self.node1, self.node2, {}), Edge(self.node2, self.node3, {}), Edge(self.node3, self.node1, {})]
        graph = Graph(self.nodes,edges)
        tree = Tree(None).from_graph(graph, self.node1.node_id)

        self.assertEqual(tree.root.node_id, self.node1.node_id)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].node_id, self.node2.node_id)
        self.assertEqual(len(tree.root.children[0].children), 1)
        self.assertEqual(tree.root.children[0].children[0].node_id, self.node3.node_id)
        self.assertEqual(len(tree.root.children[0].children[0].children), 0)

if __name__ == '__main__':
    unittest.main()
