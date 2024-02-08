import os.path

from graph_visualizer_api.datasource import DataSource
from graph_visualizer_api.model.exceptions import GraphError
from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.node import Node
from graph_visualizer_api.model.edge import Edge

from typing import Any, List, Optional

from json_data_source_plugin.provider import provide_json_data


class JsonDataSource(DataSource):
    """Generic JSON to Graph Parser.

    Attributes:
        _json_data: JSON data to be parsed.
        _next_node_id: Assigned to the next node.
        _node_cap: Maximum number of nodes.
        _graph: Parsed graph.
    """

    def __init__(self, node_cap: int = 2000):
        self._json_data = provide_json_data(os.path.join(os.path.dirname(__file__), "..", "..", "data.json"))
        self._next_node_id = 1
        self._node_cap = node_cap
        self._graph = Graph([], [])

    @property
    def configuration(self) -> Optional[dict[str, Any]]:
        return {}

    @configuration.setter
    def configuration(self, configuration: dict[str, Any]):
        pass

    def _process_node(self, nodes: List, edges: List) -> None:
        """Processes JSON data to create nodes and edges.

        This is a method for parsing nodes and edges

        :param nodes: List of json dicts representing node data
        :param edges: List of json dicts representing edge data
        """
        for node_data in nodes:
            node = Node(node_data["id"], {"name": node_data["name"]})
            self._graph.add_node(node)


        for edge_data in edges:
            source = self._graph.get_node_by_id(edge_data["source"])
            target = self._graph.get_node_by_id(edge_data["target"])

            edge = Edge(source, target, {})
            self._graph.add_edge(edge)

            if(edge_data["bi_directional"] == True):
                reverse_edge = Edge(target, source, {})
                self._graph.add_edge(reverse_edge)
    

    def generate_graph(self) -> Graph:
        """Creates the graph.

        :return: Graph object.
        """
        print("Parsing JSON data and building graph...")
        try:
            self._process_node(self._json_data["nodes"], self._json_data["edges"])
        except GraphError:
            print('Returning existing graph...')

        return self._graph
