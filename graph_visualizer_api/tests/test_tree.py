import unittest
from graph_visualizer_api.model.node import Node
from graph_visualizer_api.model.edge import Edge
from graph_visualizer_api.model.tree import Tree

class TestTree(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(1, {})
        self.node2 = Node(2, {})
        self.node3 = Node(3, {})

    def test_update_tree_undirected(self):
        edges = [Edge(self.node1, self.node2, {}), Edge(self.node2, self.node3, {})]
        tree = Tree(self.node1, directed=False)
        tree.update_tree(self.node1, edges)

        self.assertEqual(tree.root.node, self.node1)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].node, self.node2)
        self.assertEqual(len(tree.root.children[0].children), 1)
        self.assertEqual(tree.root.children[0].children[0].node, self.node3)
        self.assertEqual(len(tree.root.children[0].children[0].children), 0)

    def test_update_tree_directed(self):
        edges = [Edge(self.node1, self.node2, {}), Edge(self.node2, self.node3, {})]
        tree = Tree(self.node1, directed=True)
        tree.update_tree(self.node1, edges)

        self.assertEqual(tree.root.node, self.node1)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].node, self.node2)
        self.assertEqual(len(tree.root.children[0].children), 1)
        self.assertEqual(tree.root.children[0].children[0].node, self.node3)
        self.assertEqual(len(tree.root.children[0].children[0].children), 0)

    def test_update_tree_mixed_undirected(self):
        edges = [Edge(self.node1, self.node2, {}), Edge(self.node2, self.node3, {}), Edge(self.node3, self.node1, {})]
        tree = Tree(self.node1, directed=False)
        tree.update_tree(self.node1, edges)

        self.assertEqual(tree.root.node, self.node1)
        self.assertEqual(len(tree.root.children), 2)
        self.assertEqual(tree.root.children[0].node, self.node2)
        self.assertEqual(tree.root.children[1].node, self.node3)
        self.assertEqual(len(tree.root.children[0].children), 1)
        self.assertEqual(len(tree.root.children[1].children), 1)

    def test_update_tree_mixed_directed(self):
        edges = [Edge(self.node1, self.node2, {}), Edge(self.node2, self.node3, {}), Edge(self.node3, self.node1, {})]
        tree = Tree(self.node1, directed=True)
        tree.update_tree(self.node1, edges)

        self.assertEqual(tree.root.node, self.node1)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].node, self.node2)
        self.assertEqual(len(tree.root.children[0].children), 1)
        self.assertEqual(tree.root.children[0].children[0].node, self.node3)
        self.assertEqual(len(tree.root.children[0].children[0].children), 0)

if __name__ == '__main__':
    unittest.main()
