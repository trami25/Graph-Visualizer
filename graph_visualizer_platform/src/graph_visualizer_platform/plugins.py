from __future__ import annotations

from abc import ABC, abstractmethod

from graph_visualizer_api.datasource import DataSource
from graph_visualizer_api.visualizer import Visualizer
from typing import TypeVar, Type, Generic, Any
from graph_visualizer_platform.exceptions import PluginException
from graph_visualizer_platform.singleton import SingletonMeta

import sys

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

T = TypeVar('T')


class PluginListener(ABC):
    @abstractmethod
    def on_config_changed(self):
        pass


class Plugin(Generic[T]):
    """Model of a plugin.

    Attributes:
        _name: Name of the plugin.
        _plugin_type: The plugin class.
        _instance: The instance of the plugin.
        called.
        _listeners: List of plugin listeners.
    """

    def __init__(self, name: str, plugin_type: Type[T], instance: T = None):
        self._name = name
        self._plugin_type = plugin_type
        self._instance = instance
        self._listeners: list[PluginListener] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def instance(self) -> T:
        if self._instance is None:
            self._instance = self._plugin_type()

        return self._instance

    def add_listener(self, listener: PluginListener) -> None:
        """Add a listener to the list of plugin listeners.

        :param listener: New listener to be added to the list.
        """

        self._listeners.append(listener)

    def remove_listener(self, listener: PluginListener) -> None:
        """Remove listener from the list of plugin listeners.

        :param listener: Listener to be removed.
        """

        self._listeners.remove(listener)

    def update_configuration(self, configuration: dict[str, Any]) -> None:
        """Updates the plugin configuration

        :param configuration: New configuration.
        """

        instance = self.instance
        instance.configuration = configuration
        for listener in self._listeners:
            listener.on_config_changed()

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


class PluginManager(metaclass=SingletonMeta):
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

    @property
    def data_sources(self) -> tuple[Plugin[DataSource], ...]:
        return tuple(self._data_sources)

    @property
    def visualizers(self) -> tuple[Plugin[Visualizer], ...]:
        return tuple(self._visualizers)

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
