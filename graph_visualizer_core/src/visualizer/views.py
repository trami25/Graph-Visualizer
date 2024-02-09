from django.shortcuts import render, redirect
from django.apps.registry import apps
from django.http import Http404, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.safestring import mark_safe
from graph_visualizer_platform.plugins import PluginManager
from graph_visualizer_platform.workspaces import WorkspaceManager
from graph_visualizer_platform.exceptions import WorkspaceException, PluginException


# Create your views here.
def index(request):
    workspaces = apps.get_app_config('visualizer').workspaces
    visualizer_plugins = apps.get_app_config('visualizer').visualizer_plugins
    data_source_plugins = apps.get_app_config('visualizer').data_source_plugins

    return render(request, 'visualizer/base.html',
                  context={
                      'workspaces': workspaces,
                      'visualizer_plugins': visualizer_plugins,
                      'data_source_plugins': data_source_plugins
                  })


def workspace_view(request, tag):
    data_source_plugins = apps.get_app_config('visualizer').data_source_plugins
    visualizer_plugins = apps.get_app_config('visualizer').visualizer_plugins
    workspaces = apps.get_app_config('visualizer').workspaces

    workspace_manager = WorkspaceManager()
    active_workspace = workspace_manager.get_by_tag(tag)
    if active_workspace is None:
        raise Http404('Workspace does not exist.')
    my_template = active_workspace.template

    my_tree = active_workspace._tree_template
    return render(request, 'visualizer/workspace.html',
                  context={
                      'data_source_plugins': data_source_plugins,
                      'visualizer_plugins': visualizer_plugins,
                      'workspaces': workspaces,
                      'active_workspace': active_workspace,
                      'template': mark_safe(my_template),
                      'tree_template':mark_safe(my_tree)
                  })


def new_workspace(request):
    workspace_manager = WorkspaceManager()
    plugin_manager = PluginManager()

    if len(request.POST['tag']) <= 0:  # TODO: maybe add this to workspace manager?
        return HttpResponseBadRequest('Tag cannot be empty.')

    try:
        selected_data_source = request.POST['datasource']
        selected_visualizer = request.POST['visualizer']
    except MultiValueDictKeyError:
        return HttpResponseBadRequest('No data source or visualizer selected.')

    try:
        workspace_manager.spawn(request.POST['tag'], plugin_manager.get_data_source_by_name(selected_data_source),
                                plugin_manager.get_visualizer_by_name(selected_visualizer))
    except (WorkspaceException, PluginException) as e:
        return HttpResponseBadRequest(e)

    return redirect('workspace', tag=request.POST['tag'])


def remove_workspace(request):
    workspace_manager = WorkspaceManager()

    if len(request.POST['tag']) <= 0:
        return HttpResponseBadRequest('Tag cannot be empty.')

    try:
        workspace_manager.kill(request.POST['tag'])
    except WorkspaceException as e:
        return HttpResponseBadRequest(e)

    return redirect('index')


def workspace_plugins(request, tag):
    workspace_manager = WorkspaceManager()
    plugin_manager = PluginManager()

    workspace = workspace_manager.get_by_tag(tag)

    if request.POST['source'] != workspace.active_data_source.name:
        workspace.active_data_source = plugin_manager.get_data_source_by_name(request.POST['source'])

    if request.POST['visualizer'] != workspace.active_visualizer.name:
        workspace.active_visualizer = plugin_manager.get_visualizer_by_name(request.POST['visualizer'])

    return redirect('workspace', tag=tag)


def plugin_config(request, name):
    plugin_manager = PluginManager()

    try:
        plugin = plugin_manager.get_data_source_by_name(name)
    except PluginException as e:
        raise Http404(e)

    configuration_options = [(config_key, config_val) for config_key, config_val in
                             plugin.instance.configuration.items()]

    return render(request, 'visualizer/config.html', context={
        'name': plugin.name,
        'options': configuration_options
    })


def plugin_config_update(request, name):
    plugin_manager = PluginManager()

    try:
        plugin = plugin_manager.get_data_source_by_name(name)
    except PluginException as e:
        raise Http404(e)

    new_config = {}
    for key in plugin.instance.configuration.keys():
        if not request.POST[key]:
            return HttpResponseBadRequest('No blank fields!')
        new_config[key] = request.POST[key]

    plugin.instance.configuration = new_config

    return redirect('index')


def add_filter(request, tag):
    workspace_manager = WorkspaceManager()

    workspace = workspace_manager.get_by_tag(tag)

    attribute_name = request.POST['attribute_name']
    comparator = request.POST['comparator']
    attribute_value = request.POST['attribute_value']
    filter_name = attribute_name + " " + comparator + " " + attribute_value

    try:
        workspace.graph_store.add_filter(filter_name)
    except ValueError:
        return HttpResponseBadRequest("Invalid filter format. Please fill all fields.")

    print(len(workspace.graph_store.subgraph.nodes))
    print(len(workspace.graph_store.filters))

    return redirect('workspace', tag=tag)


def remove_filter(request, tag):
    workspace_manager = WorkspaceManager()

    workspace = workspace_manager.get_by_tag(tag)

    if 'filters' in request.POST:
        filter_name = request.POST['filters']
        try:
            workspace.graph_store.remove_filter(filter_name)
        except ValueError:
            return HttpResponseBadRequest("Invalid filter format. Please fill all fields.")
    else:
        return HttpResponseBadRequest("No filter selected.")

    print(len(workspace.graph_store.subgraph.nodes))
    print(len(workspace.graph_store.filters))

    return redirect('workspace', tag=tag)