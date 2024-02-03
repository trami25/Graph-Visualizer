import os
import unittest
import django
from graph_visualizer_api.model.graph import Graph, Node, Edge
from simple_visualizer_plugin.simple_visualizer import SimpleVisualizer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graph_visualizer_core.settings')
django.setup()


class TestSimpleVisualizer(unittest.TestCase):

    def assertHtmlContains(self, expected_html, actual_html):
        expected_stripped = "".join(expected_html.split())
        actual_stripped = "".join(actual_html.split())
        self.assertEqual(expected_stripped, actual_stripped)

    def test_generate_template(self):
        node1 = Node(1, {"first": "John", "last": "Doe", "years": 53})
        node2 = Node(2, {"first": "Mike", "last": "Doe", "years": 25})
        node3 = Node(3, {"first": "Lucy", "last": "Doe", "years": 15})

        edge1 = Edge(node1, node2, {})
        edge2 = Edge(node1, node3, {})

        graph = Graph([node1, node2, node3], [edge1, edge2])

        visualizer = SimpleVisualizer()

        expected_result = """
                <div style='border: 1px solid black; padding: 10px; margin: 10px;'>
                    <p style='margin: 5px; padding: 5px; background-color: #f0f0f0;'>ID: 1</p>
                    <p style='margin: 5px; padding: 5px; background-color: #f0f0f0;'>ID: 2</p>
                    <p style='margin: 5px; padding: 5px; background-color: #f0f0f0;'>ID: 3</p>
                </div>
                """

        actual_result = visualizer.generate_template(graph)

        self.assertHtmlContains(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
