import unittest
from unittest.mock import MagicMock, patch
from graph_visualizer_platform.workspaces import WorkspaceManager
from graph_visualizer_platform.plugins import Plugin
from graph_visualizer_api.datasource import DataSource
from graph_visualizer_api.visualizer import Visualizer
from graph_visualizer_api.model.graph import Graph
from graph_visualizer_platform.exceptions import WorkspaceException


class TestWorkspaces(unittest.TestCase):

    @patch.multiple(DataSource, __abstractmethods__=set())
    @patch.multiple(Visualizer, __abstractmethods__=set())
    def setUp(self):
        data_source_mock = DataSource()
        data_source_mock.generate_graph = MagicMock(return_value=Graph([], []))
        visualizer_mock = Visualizer()
        visualizer_mock.generate_template = MagicMock(return_value='')

        self.data_source_plugin = Plugin('test_data_source', DataSource, data_source_mock)
        self.visualizer_plugin = Plugin('test_visualizer', Visualizer, visualizer_mock)

    def test_workspace_manager_is_singleton(self):
        wm = WorkspaceManager()
        wm.spawn('tag1', self.data_source_plugin, self.visualizer_plugin)

        wm2 = WorkspaceManager()

        self.assertIsNot(0, len(wm2.workspaces))

    def test_workspace_spawn(self):
        wm = WorkspaceManager()
        wm.spawn('tag2', self.data_source_plugin, self.visualizer_plugin)

        self.assertEqual('tag2', wm.get_by_tag('tag2').tag)

    def test_workspace_spawn_exception(self):
        wm = WorkspaceManager()

        with self.assertRaises(WorkspaceException):
            wm.spawn('tag2', self.data_source_plugin, self.visualizer_plugin)

    def test_workspace_kill(self):
        wm = WorkspaceManager()
        wm.spawn('tag1', self.data_source_plugin, self.visualizer_plugin)

        wm.kill('tag1')

        self.assertEqual(0, len(wm.workspaces))

    def test_workspace_kill_exception(self):
        wm = WorkspaceManager()

        with self.assertRaises(WorkspaceException):
            wm.kill('tag5')
