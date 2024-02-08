import unittest
from datetime import timedelta, date

from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.node import Node
from graph_visualizer_api.model.edge import Edge
from graph_visualizer_api.model.filter import Filter
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

    def test_find_by_attribute(self):
        node1 = Node(1, {'name': 'Pera'})
        node2 = Node(2, {'name': 'Djura', 'age': 25})
        node3 = Node(3, {})
        node4 = Node(4, {'age': 25})
        graph = Graph([node1, node2, node3, node4], [])

        self.assertEqual(0, len(graph.get_nodes_by_attributes(job='baker')))
        self.assertEqual(2, len(graph.get_nodes_by_attributes(age=25)))
        self.assertEqual(node1, graph.get_nodes_by_attributes(name='Pera')[0])
        self.assertEqual(0, len(graph.get_nodes_by_attributes(name='Mika')))

    def test_filter_and_search(self):
        filter = Filter('search', 'contains', 'ra')
        filter2 = Filter('date', '>=', '2024-02-06')
        filter3 = Filter('age', '<', '22')
        filter4 = Filter('search', 'contains', 'ra')
        filters = [filter, filter2]

        node1 = Node(1, {'name': 'Pera', 'lastName': 'Peria', 'age': 19, "date": date.today()+timedelta(1)})
        node2 = Node(2, {'name': 'Djura', 'lastName': 'Perib', 'age': 20, "date": date.today()+timedelta(2)})
        node3 = Node(3, {'name': 'Pera', 'lastName': 'Peric', 'age': 21, "date": date.today()-timedelta(2)})
        node4 = Node(4, {'name': 'Pera', 'lastName': 'Perid', 'age': 22, "date": date.today()-timedelta(2)})
        node5 = Node(5, {'name': 'Mika', 'lastName': 'Perie', 'age': 23, "date": date.today()+timedelta(1)})

        edge1 = Edge(node1, node2, {})
        edge2 = Edge(node2, node3, {})
        edge3 = Edge(node3, node4, {})
        graph = Graph([node1, node2, node3, node4, node5], [edge1, edge2, edge3])

        self.assertEqual(2, len(graph.search_and_filer(filters).nodes))
        self.assertEqual(3, len(graph.search_and_filer([filter3]).nodes))
        self.assertEqual(4, len(graph.search_and_filer([filter4]).nodes))
