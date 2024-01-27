import unittest
from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.node import Node
from graph_visualizer_api.model.edge import Edge
from graph_visualizer_api.model.exceptions import GraphError


class TestGraph(unittest.TestCase):
    def test_get_node_when_exists(self):
        nodes = [Node(1, {}), Node(2, {})]
        graph = Graph(nodes, [])

        node = graph.get_node_by_id(1)

        self.assertEqual(nodes[0], node)

    def test_get_node_when_not_exists(self):
        graph = Graph([], [])

        node = graph.get_node_by_id(1)

        self.assertIsNone(node)

    def test_get_edge_when_exists(self):
        source = Node(1, {})
        target = Node(2, {})
        edges = [Edge(source, target, {})]
        graph = Graph([source, target], edges)

        edge = graph.get_edge(source, target)

        self.assertEqual(edges[0], edge)

    def test_get_edge_when_not_exists(self):
        source = Node(1, {})
        target = Node(2, {})
        graph = Graph([source, target], [])

        edge = graph.get_edge(source, target)

        self.assertIsNone(edge)

    def test_graph_init_raises_exception_when_edge_node_not_in_nodes(self):
        node1 = Node(1, {})
        node2 = Node(2, {})
        edge = Edge(node1, node2, {})

        with self.assertRaises(GraphError):
            graph = Graph([node1], [edge])

    def test_add_node_when_exists(self):
        node = Node(1, {})
        graph = Graph([node], [])

        with self.assertRaises(GraphError):
            graph.add_node(node)

    def test_add_node_when_not_exists(self):
        node = Node(1, {})
        graph = Graph([], [])

        graph.add_node(node)

        self.assertEqual(1, len(graph.nodes))
        self.assertEqual(node, graph.get_node_by_id(node.node_id))

    def test_remove_node_when_exists(self):
        node = Node(1, {})
        graph = Graph([node], [])

        graph.remove_node(node)

        self.assertEqual(0, len(graph.nodes))
        self.assertIsNone(graph.get_node_by_id(node.node_id))

    def test_remove_node_when_not_exists(self):
        node = Node(1, {})
        graph = Graph([], [])

        with self.assertRaises(GraphError):
            graph.remove_node(node)

    def test_add_edge_when_exists(self):
        node1 = Node(1, {})
        node2 = Node(2, {})
        edge = Edge(node1, node2, {})
        graph = Graph([node1, node2], [edge])

        with self.assertRaises(GraphError):
            graph.add_edge(edge)

    def test_add_edge_when_not_exists(self):
        node1 = Node(1, {})
        node2 = Node(2, {})
        edge = Edge(node1, node2, {})
        graph = Graph([node1, node2], [])

        graph.add_edge(edge)

        self.assertEqual(1, len(graph.edges))
        self.assertEqual(edge, graph.get_edge(node1, node2))

    def test_remove_edge_when_not_exists(self):
        node1 = Node(1, {})
        node2 = Node(2, {})
        edge = Edge(node1, node2, {})
        graph = Graph([node1, node2], [])

        with self.assertRaises(GraphError):
            graph.remove_edge(edge)

    def test_remove_edge_when_exists(self):
        node1 = Node(1, {})
        node2 = Node(2, {})
        edge = Edge(node1, node2, {})
        graph = Graph([node1, node2], [edge])

        graph.remove_edge(edge)

        self.assertEqual(0, len(graph.edges))
        self.assertIsNone(graph.get_edge(node1, node2))
