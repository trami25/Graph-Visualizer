from abc import ABC, abstractmethod
from graph_visualizer_api.model.graph import Graph


class DataSource(ABC):
    """Data source abstraction.

    Serves as an abstraction of the data source. There is only one required method: generate_graph(). It should
    return a Graph object.
    """

    @abstractmethod
    def generate_graph(self) -> Graph:
        """Generates a graph.

        :returns: A Graph object.
        """
        pass
