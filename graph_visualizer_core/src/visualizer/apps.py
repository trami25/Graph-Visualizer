from django.apps import AppConfig
from graph_visualizer_platform.plugins import PluginManager


class VisualizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visualizer'
    data_source_plugins = []
    visualizer_plugins = []

    def ready(self):
        plugin_manager = PluginManager()
        self.data_source_plugins = plugin_manager.data_sources
        self.visualizer_plugins = plugin_manager.visualizers
