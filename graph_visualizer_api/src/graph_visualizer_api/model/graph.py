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

    def get_node_by_attribute(self, attribute: str, value: Any) -> Optional[Node]:
        """Returns a node by its attribute.

        :param attribute: Attribute of the node.
        :param value: Value for the given attribute.
        :returns: Node if found or None.
        """

        return next((node for node in self._nodes if value == node.data.get(attribute)), None)

    def __str__(self) -> str:
        nodes = ''.join([f'{node}\n' for node in self._nodes])
        edges = ''.join([f'{edge}\n' for edge in self._edges])
        return nodes + edges
