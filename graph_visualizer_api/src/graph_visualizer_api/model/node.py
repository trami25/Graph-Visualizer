from __future__ import annotations
from typing import Any


class Node:
    """Model of a node in a graph.

    Attributes:
        node_id: Unique identifier of the node.
        data: Dictionary containing key/value pairs for the node data.
    """

    def __init__(self, node_id: int, data: dict[str, Any]):
        self._node_id = node_id
        self._data = data

    @property
    def node_id(self) -> int:
        return self._node_id

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    def __eq__(self, other: Node) -> bool:
        return self._node_id == other._node_id

    def __hash__(self) -> int:
        return hash(self._node_id)