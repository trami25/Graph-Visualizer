from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.node import Node
from simple_visualizer_plugin.simple_visualizer import SimpleVisualizer

if __name__ == '__main__':
    simple_visualizer = SimpleVisualizer()
    graph = Graph([Node(1, {'name': 'Test'}), Node(2, {'name': 'Hello'})], [])
    print(simple_visualizer.generate_template(graph))