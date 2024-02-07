from django.shortcuts import render
from django.apps.registry import apps


# Create your views here.
def index(request):
    data_source_plugins = apps.get_app_config('visualizer').data_source_plugins
    visualizer_plugins = apps.get_app_config('visualizer').visualizer_plugins
    return render(request, 'visualizer/index.html', context={'data_source_plugins': data_source_plugins, 'visualizer_plugins': visualizer_plugins})
