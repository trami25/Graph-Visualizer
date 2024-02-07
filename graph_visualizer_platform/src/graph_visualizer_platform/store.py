from abc import ABC, abstractmethod
from graph_visualizer_api.model.graph import Graph
from typing import Optional


class GraphListener(ABC):
    """Graph listener interface.

    Classes interested in graph updates should implement this interface.
    """

    @abstractmethod
    def on_graph_change(self, graph: Graph):
        pass


class GraphStore:
    """Stores the graph and its filters.

    Attributes:
        _root_graph: The root graph with no filters applied.
        _subgraph: Subgraph formed from applying filters to the root graph.
        _listeners: List of graph listeners.
        # TODO: add filters...
    """

    def __init__(self):
        self._root_graph: Optional[Graph] = None
        self._subgraph: Optional[Graph] = None
        self._listeners: list[GraphListener] = []

    @property
    def root_graph(self) -> Optional[Graph]:
        return self._root_graph

    @root_graph.setter
    def root_graph(self, graph: Graph) -> None:
        self._root_graph = graph
        for listener in self._listeners:
            listener.on_graph_change(graph)

    def add_listener(self, *args: GraphListener) -> None:
        """Adds a listener to the list of listeners.

        :param args: Listeners to add to the list.
        """
        self._listeners.extend(*args)

    def add_filter(self, prompt: str) -> None:
        # TODO: add prompt parsing to filter and graph filtering...
        raise NotImplementedError

    def remove_filter(self) -> None:
        # TODO: add graph filtering...
        raise NotImplementedError

    def _parse_prompt(self, prompt: str) -> None:
        raise NotImplementedError
