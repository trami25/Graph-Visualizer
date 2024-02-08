from abc import ABC, abstractmethod
from typing import Optional

from graph_visualizer_api.model.graph import Graph


class DataSource(ABC):
    """Data source abstraction.

    Serves as an abstraction of the data source. There is only one required method: generate_graph(). It should
    return a Graph object.

    Attributes:
        configuration: The plugin configuration.
    """

    @abstractmethod
    def generate_graph(self) -> Graph:
        """Generates a graph.

        :returns: A Graph object.
        """
        pass

    @property
    @abstractmethod
    def configuration(self) -> Optional[dict[str, int | str | bool]]:
        pass

    @configuration.setter
    @abstractmethod
    def configuration(self, configuration: dict[str, int | str | bool]) -> None:
        pass
