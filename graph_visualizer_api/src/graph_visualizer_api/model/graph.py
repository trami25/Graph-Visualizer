from .filter import Filter
from .node import Node
from .edge import Edge
from .exceptions import GraphError
from typing import Optional, Any


class Graph:
    """Model of a graph.

    Simple graph model containing a list of nodes and edges.

    Attributes:
        nodes: List of nodes.
        edges: List of edges.
    """

    def __init__(self, nodes: list[Node], edges: list[Edge]):
        for edge in edges:
            if edge.source not in nodes or edge.target not in nodes:
                raise GraphError("non existent node in edge")

        self._nodes = nodes
        self._edges = edges

    @property
    def nodes(self) -> list[Node]:
        return self._nodes

    @property
    def edges(self) -> list[Edge]:
        return self._edges

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

    def search_and_filer(self, filters: list[Filter]) -> list[Node]:
        """Returns a list of nodes that satisfy the given filters.

        :param filters: List of filters to apply.
        :returns: List of nodes that satisfy the filters.
        :raise GraphError: Raised when the comparator is invalid.
        """

        nodes = []
        for node in self._nodes:
            satisfies_all_filters = True
            for filter in filters:
                if filter.attribute_name in node.data.keys():
                    if filter.comparator == '=':
                        satisfies_all_filters = node.data[filter.attribute_name] == filter.attribute_value
                    elif filter.comparator == '!=':
                        satisfies_all_filters = node.data[filter.attribute_name] != filter.attribute_value
                    elif filter.comparator == '>':
                        satisfies_all_filters = node.data[filter.attribute_name] > filter.attribute_value
                    elif filter.comparator == '<':
                        satisfies_all_filters = node.data[filter.attribute_name] < filter.attribute_value
                    elif filter.comparator == '>=':
                        satisfies_all_filters = node.data[filter.attribute_name] >= filter.attribute_value
                    elif filter.comparator == '<=':
                        satisfies_all_filters = node.data[filter.attribute_name] <= filter.attribute_value
                    elif filter.comparator == 'search':
                        satisfies_all_filters = node.data.keys().__contains__(filter.attribute_value) or node.data.values().__contains__(filter.attribute_value)
                    else:
                        raise GraphError("invalid comparator")

                if not satisfies_all_filters:
                    satisfies_all_filters = False
                    break

            if satisfies_all_filters:
                nodes.append(node)

        return nodes

    def __str__(self) -> str:
        nodes = ''.join([f'{node}\n' for node in self._nodes])
        edges = ''.join([f'{edge}\n' for edge in self._edges])
        return nodes + edges
