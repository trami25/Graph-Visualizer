from __future__ import annotations
from .node import Node
from typing import Any


class Edge:
    """Model of an edge in a graph.

    Represents a model of an edge that references two nodes in a graph: source and target.
    Can hold additional data to comform to weighted graphs.

    Attributes:
        source: The source node of the edge.
        target: The target node of the edge.
        data: The data associated with the edge.
    """

    def __init__(self, source: Node, target: Node, data: dict[str, Any]):
        self._source = source
        self._target = target
        self._data = data

    @property
    def source(self) -> Node:
        return self._source

    @property
    def target(self) -> Node:
        return self._target

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    def __eq__(self, other: Edge) -> bool:
        return self._source == other._source and self._target == other._target
