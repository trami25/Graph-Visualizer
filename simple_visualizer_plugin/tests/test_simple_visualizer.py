import os
import unittest
import django
from bs4 import BeautifulSoup

from graph_visualizer_api.model.graph import Graph, Node, Edge
from simple_visualizer_plugin.simple_visualizer import SimpleVisualizer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graph_visualizer_core.settings')
django.setup()


class TestSimpleVisualizer(unittest.TestCase):

    def assertHtmlContains(self, expected_html, actual_html):
        expected_stripped = "".join(expected_html.split())
        actual_stripped = "".join(actual_html.split())
        self.assertEqual(expected_stripped, actual_stripped)

    def test_generate_template_with_arrows(self):
        node1 = Node(1, {"first": "John", "last": "Doe", "years": 53})
        node2 = Node(2, {"first": "Mike", "last": "Doe", "years": 25})
        node3 = Node(3, {"first": "Lucy", "last": "Doe", "years": 15})

        edge1 = Edge(node1, node2, {})
        edge2 = Edge(node1, node3, {})

        graph = Graph([node1, node2, node3], [edge1, edge2])

        visualizer = SimpleVisualizer()

        expected_result = """
       <head>
 <link href="styles.css" rel="stylesheet" type="text/css"/>
 <script>
  function connectNodes(node1, node2, directed) {
            const rect1 = node1.getBoundingClientRect();
            const rect2 = node2.getBoundingClientRect();

            const line = document.createElement('div');
            line.className = 'line';
            line.style.top = (rect1.top + rect1.height / 2) + 'px';
            line.style.left = (rect1.left + rect1.width) + 'px';
            line.style.width = (rect2.left - rect1.left - rect1.width) + 'px';
            line.style.height = '2px';

            if (directed) {
                const arrow = document.createElement('div');
                arrow.className = 'arrow';
                arrow.style.position = 'absolute';
                arrow.style.top = (rect2.top + rect2.height / 2) - 5 + 'px';
                arrow.style.left = (rect2.left - 10) + 'px';
                arrow.style.width = '0';
                arrow.style.height = '0';
                arrow.style.borderLeft = '10px solid transparent';
                arrow.style.borderRight = '10px solid transparent';
                arrow.style.borderBottom = '10px solid black';
                document.body.appendChild(arrow);
            }

            document.body.appendChild(line);
        }
 </script>
</head>
<body>
 <div class="graph-container">
  <p class="node" id="node1">
   ID: 1
  </p>
  <p class="node" id="node2">
   ID: 2
  </p>
  <p class="node" id="node3">
   ID: 3
  </p>
  <div id="connected-nodes">
  </div>
 </div>
 <script>
  const node1_1 = document.getElementById('node1');
            const node2_2 = document.getElementById('node2');
            const directed = true;
            connectNodes(node1_1, node2_2, directed);
        
            const node1_1 = document.getElementById('node1');
            const node2_3 = document.getElementById('node3');
            const directed = true;
            connectNodes(node1_1, node2_3, directed);
 </script>
</body>
        """

        actual_result = visualizer.generate_template(graph)

        self.maxDiff = None
        soup_expected = BeautifulSoup(expected_result, 'html.parser')
        soup_actual = BeautifulSoup(actual_result, 'html.parser')

        self.assertEqual(soup_expected.prettify(), soup_actual.prettify())


if __name__ == '__main__':
    unittest.main()
