from django.apps import AppConfig
from graph_visualizer_platform.plugins import PluginManager
from graph_visualizer_platform.workspaces import WorkspaceManager


class VisualizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visualizer'
    data_source_plugins = []
    visualizer_plugins = []
    workspaces = []

    def ready(self):
        plugin_manager = PluginManager()
        workspace_manager = WorkspaceManager()

        self.data_source_plugins = plugin_manager.data_sources
        self.visualizer_plugins = plugin_manager.visualizers
        self.workspaces = workspace_manager.workspaces
