from graph_visualizer_platform.plugins import Plugin
from graph_visualizer_api.datasource import DataSource
from graph_visualizer_api.visualizer import Visualizer


class Workspace:
    """Workspace contains information of the current plugins, graphs and filters, and views.

    Attributes:
        _tag: The tag of the workspace.
        _active_data_source: The currently active data source plugin for this workspace.
        _active_visualizer: The currently active visualizer plugin for this workspace.
    """

    def __init__(self, tag: str, active_data_source: Plugin[DataSource], active_visualizer: Plugin[Visualizer]):
        self._tag = tag
        self.active_data_source = active_data_source
        self.active_visualizer = active_visualizer

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, value: str) -> None:
        self._tag = value

    @property
    def active_data_source(self) -> Plugin[DataSource]:
        return self._active_data_source

    @active_data_source.setter
    def active_data_source(self, value: Plugin[DataSource]) -> None:
        self._active_data_source = value
        graph = value.instance.generate_graph()
        # TODO: Set the data store graph...

    @property
    def active_visualizer(self) -> Plugin[Visualizer]:
        return self._active_visualizer

    @active_visualizer.setter
    def active_visualizer(self, value: Plugin[Visualizer]) -> None:
        self._active_visualizer = value
        # TODO: Set the plugin in MainView and generate template...
