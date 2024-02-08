from abc import ABC, abstractmethod

from graph_visualizer_api.model.filter import Filter
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
        _filters: List of filters to apply to the graph.
    """

    def __init__(self):
        self._root_graph: Optional[Graph] = None
        self._subgraph: Optional[Graph] = None
        self._listeners: list[GraphListener] = []
        self._filters: list[Filter] = []

    @property
    def root_graph(self) -> Optional[Graph]:
        return self._root_graph

    @root_graph.setter
    def root_graph(self, graph: Graph) -> None:
        self._root_graph = graph
        self._subgraph = graph
        for listener in self._listeners:
            listener.on_graph_change(graph)

    def add_listener(self, *args: GraphListener) -> None:
        """Adds a listener to the list of listeners.

        :param args: Listeners to add to the list.
        """
        self._listeners.extend(*args)

    def add_filter(self, prompt: str) -> None:
        """
        Adds a filter to the subgraph.

        :param prompt: String to parse into a filter.
        :return:
        """
        try:
            filter = self._parse_prompt(prompt)
            self._filters.append(filter)
            self._subgraph = self._subgraph.search_and_filer([filter])
        except ValueError:
            raise ValueError("Invalid filter")

    def remove_filter(self, prompt: str) -> None:
        """
        Removes a filter from the subgraph.
        :param prompt: String to parse into a filter.
        """
        try:
            filter = self._parse_prompt(prompt)
            self._filters.remove(filter)
            self._subgraph = self._root_graph.search_and_filer(self._filters)
        except ValueError:
            raise ValueError("Invalid filter")

    @staticmethod
    def _parse_prompt(prompt: str) -> Filter:
        """
        Parses a prompt into a filter.

        :param prompt: string to parse into a filter.
        :return: filter
        """
        filter_tokens = prompt.split()
        if len(filter_tokens) != 3 or filter_tokens[1] not in ['=', '!=', '>', '<', '>=', '<=', 'contains']:
            raise ValueError("Invalid filter")
        return Filter(filter_tokens[0], filter_tokens[1], filter_tokens[2])

