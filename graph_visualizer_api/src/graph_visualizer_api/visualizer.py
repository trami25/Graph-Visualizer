from abc import ABC, abstractmethod
from graph_visualizer_api.model.graph import Graph


class Visualizer(ABC):
    """Abstraction of the Visualizer plugin.

    Serves as an abstraction of the Visualizer plugin. It requires one method that should return an HTML template
    based on the provided Graph object.
    """

    @abstractmethod
    def generate_template(self, graph: Graph) -> str:
        """Generates an HTML template.

        :param graph: Graph object to be rendered.
        :returns: HTML template.
        """
        pass
