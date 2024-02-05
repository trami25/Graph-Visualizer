from __future__ import annotations
from importlib.metadata import entry_points
from graph_visualizer_api.datasource import DataSource
from graph_visualizer_api.visualizer import Visualizer
from typing import TypeVar, Type, Generic
from graph_visualizer_platform.exceptions import PluginException

T = TypeVar('T')


class Plugin(Generic[T]):
    """Model of a plugin.

    Attributes:
        _name: Name of the plugin.
        _plugin_type: The plugin class.
        _instance: The instance of the plugin. Is None when the plugin created and is only instantiated when a getter is
        called.
    """

    def __init__(self, name: str, plugin_type: Type[T]):
        self._name = name
        self._plugin_type = plugin_type
        self._instance: T = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def instance(self) -> T:
        if self._instance is None:
            self._instance = self._plugin_type()

        return self._instance

    def __str__(self):
        return f'{self._name} {self._instance}'


def load_for_group(group: str) -> list[Plugin]:
    """Loads entries by group name and transforms them to plugins.

    :param group: Name of the group.
    :return: List of plugins.
    """

    entries = entry_points(group=group)
    plugins = [Plugin(entry.name, entry.load()) for entry in entries]

    return plugins


class PluginManager:
    """Manages the plugins from the environment

    This class upon creation loads the plugins from the python environment and stores them in lists.
    It provides two methods for fetching the plugins.

    Attributes:
        _data_sources: Data source plugins.
        _visualizers: Visualizer plugins.
    """

    def __init__(self):
        self._data_sources: list[Plugin[DataSource]] = load_for_group('gv.plugins.datasource')
        self._visualizers: list[Plugin[Visualizer]] = load_for_group('gv.plugins.visualizer')

    def get_data_source_by_name(self, name: str) -> Plugin[DataSource]:
        """Gets the plugin from the data source plugins.

        :param name: Name of the plugin.
        :return: The plugin matching the name.
        :raise PluginError: If the plugin is not found.
        """

        found_plugin = next((plugin for plugin in self._data_sources if name == plugin.name), None)
        if found_plugin is None:
            raise PluginException(f'no data source with name {name} found')

        return found_plugin

    def get_visualizer_by_name(self, name: str) -> Plugin[Visualizer]:
        """Gets the plugin from the visualizer plugins.

        :param name: Name of the plugin.
        :return: The plugin matching the name.
        :raise PluginError: If the plugin is not found.
        """

        found_plugin = next((plugin for plugin in self._visualizers if name == plugin.name), None)
        if found_plugin is None:
            raise PluginException(f'no visualizer with name {name} found')

        return found_plugin
