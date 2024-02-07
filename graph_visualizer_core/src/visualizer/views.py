from django.shortcuts import render, redirect
from django.apps.registry import apps
from django.http import Http404, HttpResponseBadRequest

from graph_visualizer_platform.plugins import PluginManager
from graph_visualizer_platform.workspaces import WorkspaceManager


# Create your views here.
def index(request):
    data_source_plugins = apps.get_app_config('visualizer').data_source_plugins
    visualizer_plugins = apps.get_app_config('visualizer').visualizer_plugins
    workspaces = apps.get_app_config('visualizer').workspaces
    return render(request, 'visualizer/base.html',
                  context={
                      'data_source_plugins': data_source_plugins,
                      'visualizer_plugins': visualizer_plugins,
                      'workspaces': workspaces
                  })


def workspace_view(request, tag):
    data_source_plugins = apps.get_app_config('visualizer').data_source_plugins
    visualizer_plugins = apps.get_app_config('visualizer').visualizer_plugins
    workspaces = apps.get_app_config('visualizer').workspaces

    workspace_manager = WorkspaceManager()
    active_workspace = workspace_manager.get_by_tag(tag)
    if active_workspace is None:
        raise Http404('Workspace does not exist.')

    return render(request, 'visualizer/workspace.html',
                  context={
                      'data_source_plugins': data_source_plugins,
                      'visualizer_plugins': visualizer_plugins,
                      'workspaces': workspaces,
                      'active_workspace': active_workspace
                  })


def new_workspace(request):
    workspace_manager = WorkspaceManager()
    plugin_manager = PluginManager()

    workspace = workspace_manager.get_by_tag(request.POST['tag'])
    if workspace is not None:
        return HttpResponseBadRequest('Workspace already exists.')

    workspace_manager.spawn(request.POST['tag'], plugin_manager.get_data_source_by_name('html'),
                            plugin_manager.get_visualizer_by_name('simple'))

    return redirect('index')
