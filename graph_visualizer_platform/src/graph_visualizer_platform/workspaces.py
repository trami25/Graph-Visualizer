from graph_visualizer_platform.plugins import Plugin
from graph_visualizer_api.datasource import DataSource
from graph_visualizer_api.visualizer import Visualizer
from graph_visualizer_platform.singleton import SingletonMeta
from graph_visualizer_platform.exceptions import WorkspaceException
from typing import ItemsView, Optional


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


class WorkspaceManager(metaclass=SingletonMeta):
    def __init__(self):
        self._workspaces: dict[str, Workspace] = {}

    @property
    def workspaces(self) -> ItemsView[str, Workspace]:
        return self._workspaces.items()

    def get_by_tag(self, tag: str) -> Optional[Workspace]:
        return self._workspaces.get(tag)

    def spawn(self, tag: str, data_source: Plugin[DataSource], visualizer: Plugin[Visualizer]) -> None:
        if self._workspaces.get(tag) is not None:
            raise WorkspaceException(f'workspace with tag {tag} already exists')

        workspace = Workspace(tag, data_source, visualizer)
        self._workspaces[tag] = workspace

    def kill(self, tag: str) -> None:
        try:
            del self._workspaces[tag]
        except KeyError as e:
            raise WorkspaceException(f'workspace with tag {tag} does not exist') from e
