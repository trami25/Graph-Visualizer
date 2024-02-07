from django.shortcuts import render
from django.apps.registry import apps
from django.http import Http404
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
