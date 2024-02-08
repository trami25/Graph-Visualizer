import unittest

from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.node import Node
from graph_visualizer_platform.store import GraphStore

class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = GraphStore()
        node1 = Node(1, {"name": 'test', "age": 1})
        node2 = Node(2, {"name": 'test', "age": 2})
        node3 = Node(3, {"name": 'test2', "age": 3})
        self.store.root_graph = Graph([node1, node2, node3], [])

    def test_add_filter_valid_filters(self):
        string_filter = "name = test"
        string_filter2 = "search contains 2"
        self.store.add_filter(string_filter)
        self.store.add_filter(string_filter2)

        self.assertEqual(2, len(self.store._filters))
        self.assertEqual(1, len(self.store._subgraph.nodes))

    def test_add_filter_invalid_filter(self):
        string_filter = "name= test"
        string_filter2 = "search contains 2"
        self.store.add_filter(string_filter)
        self.store.add_filter(string_filter2)

        self.assertEqual(1, len(self.store._filters))
        self.assertEqual(2, len(self.store._subgraph.nodes))

    def test_add_filter_invalid_filters(self):
        # self.store._root_graph = Graph([node1, node2], [])
        string_filter = "name = test e"
        string_filter2 = "search contains2"
        self.store.add_filter(string_filter)
        self.store.add_filter(string_filter2)

        self.assertEqual(0, len(self.store._filters))
        self.assertEqual(3, len(self.store._subgraph.nodes))

    def test_remove_filter_valid(self):
        string_filter = "name = test"
        string_filter2 = "search contains 2"
        self.store.add_filter(string_filter)
        self.store.add_filter(string_filter2)
        self.store.remove_filter(string_filter)
        self.assertEqual(1, len(self.store._filters))
        self.assertEqual(2, len(self.store._subgraph.nodes))

    def test_remove_filter_invalid_filter(self):
        string_filter = "name = test"
        string_filter2 = "search contains 2 e"
        self.store.add_filter(string_filter)
        self.store.add_filter(string_filter2)
        self.store.remove_filter(string_filter)
        self.assertEqual(0, len(self.store._filters))
        self.assertEqual(3, len(self.store._subgraph.nodes))

    def test_remove_filter_mix(self):
        string_filter = "name = test"
        string_filter2 = "search contains 2"
        self.store.add_filter(string_filter)
        self.store.add_filter(string_filter2)
        self.store.remove_filter(string_filter)
        self.store.add_filter(string_filter)
        self.assertEqual(2, len(self.store._filters))
        self.assertEqual(1, len(self.store._subgraph.nodes))