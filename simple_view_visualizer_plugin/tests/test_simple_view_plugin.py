import unittest
import os
import django
from django.template.loader import render_to_string
from simple_view_visualizer_plugin import SimpleViewVisualizer
from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.node import Node
from graph_visualizer_api.model.edge import Edge

os.environ['DJANGO_SETTINGS_MODULE'] = 'graph_visualizer_core.settings'
django.setup()


class TestSimpleViewVisualizer(unittest.TestCase):
    def test_generate_template(self):
        # Create a sample graph
        node1 = Node(1, {})
        node2 = Node(2, {})
        edge = Edge(node1, node2, {})
        graph = Graph([node1, node2], [edge])

        # Create an instance of the visualizer
        visualizer = SimpleViewVisualizer()

        # Generate HTML output from the visualizer
        html_output = visualizer.generate_template(graph)

        # Generate expected HTML output using Django's render_to_string
        expected_output = render_to_string('simple_view_visualizer_plugin/simple_view.html', {'graph_data': graph.nodes()})

        # Compare the generated output with the expected output
        self.assertEqual(html_output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()