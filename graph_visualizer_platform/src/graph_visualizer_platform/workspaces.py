from graph_visualizer_platform.plugins import Plugin
from graph_visualizer_api.datasource import DataSource
from graph_visualizer_api.visualizer import Visualizer
from graph_visualizer_platform.singleton import SingletonMeta
from graph_visualizer_platform.exceptions import WorkspaceException
from typing import ItemsView, Optional
from graph_visualizer_platform.store import GraphStore
from . import tree_view


class Workspace:
    """Workspace contains information of the current plugins, graphs and filters, and views.

    Attributes:
        _tag: The tag of the workspace.
        _active_data_source: The currently active data source plugin for this workspace.
        _active_visualizer: The currently active visualizer plugin for this workspace.
        _graph_store: Graph store for the current workspace.
        _template: The current template for the current workspace.
    """

    def __init__(self, tag: str, active_data_source: Plugin[DataSource], active_visualizer: Plugin[Visualizer]):
        self._tag = tag
        self._graph_store: GraphStore = GraphStore()
        self._active_data_source = active_data_source
        self._graph_store.root_graph = active_data_source.instance.generate_graph()
        self._active_visualizer = active_visualizer
        self._template = active_visualizer.instance.generate_template(self._graph_store.root_graph)
        self._tree_template = tree_view.generate_template(self._graph_store.root_graph)

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
        self._graph_store.root_graph = graph
        self._template = self.active_visualizer.instance.generate_template(graph)
        self._tree_template = tree_view.generate_template(graph)
        

    @property
    def active_visualizer(self) -> Plugin[Visualizer]:
        return self._active_visualizer

    @active_visualizer.setter
    def active_visualizer(self, value: Plugin[Visualizer]) -> None:
        self._active_visualizer = value
        self._template = value.instance.generate_template(self._graph_store.subgraph)
        self._tree_template = tree_view.generate_template(self._graph_store.subgraph)

    @property
    def template(self) -> str:
        return self._template


class WorkspaceManager(metaclass=SingletonMeta):
    """Manages workspaces.

    Attributes:
        _workspaces: List of existing workspaces.
    """
    def __init__(self):
        self._workspaces: dict[str, Workspace] = {}

    @property
    def workspaces(self) -> ItemsView[str, Workspace]:
        return self._workspaces.items()

    def get_by_tag(self, tag: str) -> Optional[Workspace]:
        """Gets workspace by tag

        :param tag: Tag to search workspaces by.
        :return: Workspace or None if there is no matching tag.
        """

        return self._workspaces.get(tag)

    def spawn(self, tag: str, data_source: Plugin[DataSource], visualizer: Plugin[Visualizer]) -> None:
        """Create a new workspace.

        :param tag: Tag for the new workspace.
        :param data_source: Data source that the new workspace will use.
        :param visualizer: Visualizer that the new workspace will use.
        :raise WorkspaceException: Raised when the workspace with the given tag already exists.
        """

        if self._workspaces.get(tag) is not None:
            raise WorkspaceException(f'workspace with tag {tag} already exists')

        workspace = Workspace(tag, data_source, visualizer)
        self._workspaces[tag] = workspace

    def kill(self, tag: str) -> None:
        """Remove an existing workspace.

        :param tag: Tag of the workspace to be removed.
        :raise WorkspaceException: Raised when the workspace with the given tag does not exist.
        """

        try:
            del self._workspaces[tag]
        except KeyError as e:
            raise WorkspaceException(f'workspace with tag {tag} does not exist') from e
