import unittest
from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.tree import Tree, TreeNode
from graph_visualizer_api.model.node import Node
from graph_visualizer_api.model.edge import Edge

class TestTree(unittest.TestCase):
    def test_update_tree_with_existing_node(self):
        node1 = Node(1, {})
        node2 = Node(2, {})
        node3 = Node(3, {})
        edge1 = Edge(node1, node2, {})
        edge2 = Edge(node1, node3, {})
        graph_edges = [edge1, edge2]

        tree = Tree(node1)
        tree.update_tree(node2, graph_edges)


        self.assertEqual(tree.root.node, node2)
        self.assertEqual(len(tree.root.children), 0)


    def test_update_tree_with_nonexistent_node(self):
        node1 = Node(1, {})
        graph_edges = []

        tree = Tree(node1)
        tree.update_tree(Node(2, {}), graph_edges)


        self.assertNotEqual(tree.root.node, node1)
        self.assertEqual(len(tree.root.children), 0)

    def test_update_tree_with_cyclic_graph(self):
        node1 = Node(1, {})
        node2 = Node(2, {})
        node3 = Node(3, {})
        edge1 = Edge(node1, node2, {})
        edge2 = Edge(node2, node3, {})
        edge3 = Edge(node3, node1, {})  # Creating a cycle
        graph_edges = [edge1, edge2, edge3]

        tree = Tree(node1)
        tree.update_tree(node1, graph_edges)


        self.assertEqual(tree.root.node, node1)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].node, node2)
        self.assertEqual(len(tree.root.children[0].children), 1)
        self.assertEqual(tree.root.children[0].children[0].node, node3)



if __name__ == '__main__':
    unittest.main()
