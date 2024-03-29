from __future__ import annotations
from .filter import Filter
from .node import Node
from .edge import Edge
from .exceptions import GraphError
from typing import Optional, Any
import random


class Graph:
    """Model of a graph.

    Simple graph model containing a list of nodes and edges.

    Attributes:
        nodes: List of nodes.
        edges: List of edges.
        directed: Boolean indicating if the graph is directed.
    """

    def __init__(self, nodes: list[Node], edges: list[Edge], directed: bool = False):
        for edge in edges:
            if edge.source not in nodes or edge.target not in nodes:
                raise GraphError("non existent node in edge")

        self._nodes = nodes
        self._edges = edges
        self._directed = directed

    @property
    def nodes(self) -> list[Node]:
        return self._nodes

    @property
    def edges(self) -> list[Edge]:
        return self._edges

    @property
    def directed(self) -> bool:
        return self._directed

    def add_node(self, node: Node) -> None:
        """Add a node to the graph.

        :param node: Node to add to the graph.
        :raises GraphError: Raised when the node with the same id already exists.
        """

        if node in self._nodes:
            raise GraphError("node already exists")

        self._nodes.append(node)

    def remove_node(self, node: Node) -> None:
        """Remove a node from the graph.

        :param node: Node to be removed.
        :raises GraphError: Raised when the node with the given id does not exist.
        """

        if node not in self._nodes:
            raise GraphError("node does not exist")

        self._nodes.remove(node)

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph.

        :param edge: Edge to add to the graph.
        :raises GraphError: Raised when the edge already exists.
        """

        if edge in self._edges:
            raise GraphError("edge already exists")

        self._edges.append(edge)

    def remove_edge(self, edge: Edge) -> None:
        """Remove an edge from the graph.

        :param edge: Edge to remove.
        :raises GraphError: Raised when the edge does not exist.
        """

        if edge not in self._edges:
            raise GraphError("edge does not exist")

        self._edges.remove(edge)

    def get_node_by_id(self, node_id: int) -> Optional[Node]:
        """Returns a node by its id.

        :param node_id: Identity of the node.
        :returns: Node if found or None.
        """

        return next((node for node in self._nodes if node_id == node.node_id), None)

    def get_edge(self, source: Node, target: Node) -> Optional[Edge]:
        """Returns an edge by its source and target.

        :param source: Source node
        :param target: Target node
        :returns: Edge if found or None
        :raises GraphError: Raised when source or target do not exist
        """

        if source not in self._nodes:
            raise GraphError("source node does not exist")
        elif target not in self._nodes:
            raise GraphError("target node does not exist")

        return next((edge for edge in self._edges if source == edge.source and target == edge.target), None)

    def get_nodes_by_attributes(self, **kwargs) -> list[Node]:
        """Returns a list of nodes by their attributes.
        Checks if the given argument dictionary is a subset of the node data.

        :param kwargs: Dictionary of key/values that are used to filter nodes.
        :returns: Node if found or None.
        """

        return [node for node in self._nodes if kwargs.items() <= node.data.items()]

    def search_and_filter(self, filters: list[Filter]) -> Graph:
        """Returns a list of nodes that satisfy the given filters.

        :param filters: List of filters to apply.
        :returns: Subgraph containing nodes and edges that satisfy the filters.
        :raise GraphError: Raised when the comparator is invalid.
        """

        nodes = []
        if len(filters) == 0:
            return self
        for node in self._nodes:
            satisfies_all_filters = False
            for filter in filters:
                if filter.attribute_name in node.data.keys() or filter.attribute_name == 'search':
                    if filter.comparator == ':':
                        list_of_values = [item for pair in node.data.items() for item in pair]
                        list_of_values.append(str(node.node_id))
                        satisfies_all_filters = filter.strategy.satisfies_filter(list_of_values, filter.attribute_value)
                    else:
                        satisfies_all_filters = filter.strategy.satisfies_filter(node.data[filter.attribute_name], filter.attribute_value)

                elif filter.attribute_name == 'node_id':
                    satisfies_all_filters = filter.strategy.satisfies_filter(node.node_id, filter.attribute_value)

                if not satisfies_all_filters:
                    satisfies_all_filters = False
                    break

            if satisfies_all_filters:
                nodes.append(node)

        return Graph(nodes, self.add_edges(nodes), self._directed)

    def add_edges(self, nodes: list[Node]) -> list[Edge]:
        """Add edges between nodes in the graph.

        :param nodes: List of nodes to connect with edges.
        :returns: List of edges that were added.
        """

        edges = []
        for edge in self._edges:
            if edge.source in nodes and edge.target in nodes:
                edges.append(edge)

        return edges

    def __str__(self) -> str:
        nodes = ''.join([f'{node}\n' for node in self._nodes])
        edges = ''.join([f'{edge}\n' for edge in self._edges])
        return nodes + edges


    def get_random_node(self) -> Optional[Node]:
        """Get a random node from the graph.

        :returns: Random node from the graph, or None if the graph is empty.
        """
        if not self.nodes:
            return None
        return random.choice(self.nodes)