from graph_visualizer_api.model.filter import Filter
from graph_visualizer_api.model.graph import Graph
from graph_visualizer_api.model.filter_strategies import *
from typing import Optional


class GraphStore:
    """Stores the graph and its filters.

    Attributes:
        _root_graph: The root graph with no filters applied.
        _subgraph: Subgraph formed from applying filters to the root graph.
        _filters: List of filters to apply to the graph.
    """

    def __init__(self):
        self._root_graph: Optional[Graph] = None
        self._subgraph: Optional[Graph] = None
        self._filters: list[Filter] = []

    @property
    def root_graph(self) -> Optional[Graph]:
        return self._root_graph

    @root_graph.setter
    def root_graph(self, graph: Graph) -> None:
        self._root_graph = graph
        self._subgraph = graph

    @property
    def subgraph(self) -> Optional[Graph]:
        return self._subgraph
    @property
    def filters(self) -> list[Filter]:
        return self._filters

    def add_filter(self, prompt: str) -> None:
        """
        Adds a filter to the subgraph.

        :param prompt: String to parse into a filter.
        :return:
        """
        try:
            filter = self._parse_prompt(prompt)
            self._filters.append(filter)
            self._subgraph = self._subgraph.search_and_filter([filter])
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
            self._subgraph = self._root_graph.search_and_filter(self._filters)
        except ValueError:
            raise ValueError("Invalid filter")

    @staticmethod
    def _parse_prompt(prompt: str) -> Filter:
        """
        Parses a prompt into a filter.

        :param prompt: string to parse into a filter.
        :return: filter
        """

        comparator_to_strategy = {
            '=': EqualsFilterStrategy(),
            '!=': NotEqualsFilterStrategy(),
            '>': GreaterThanFilterStrategy(),
            '<': LessThanFilterStrategy(),
            '>=': GreaterThanOrEqualsFilterStrategy(),
            '<=': LessThanOrEqualsFilterStrategy(),
            ':': SearchFilterStrategy()
        }
        filter_tokens = prompt.split("|")
        if len(filter_tokens) != 3 or filter_tokens[1] not in ['=', '!=', '>', '<', '>=', '<=', ':']:
            raise ValueError("Invalid filter")
        return Filter(filter_tokens[0], filter_tokens[1], filter_tokens[2], comparator_to_strategy[filter_tokens[1]])
