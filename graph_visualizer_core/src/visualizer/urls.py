from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("workspace/<str:tag>/", views.workspace_view, name="workspace"),
    path("workspace/<str:tag>/plugins/", views.workspace_plugins, name="workspace_plugins"),
    path("new/", views.new_workspace, name="new"),
    path("remove/", views.remove_workspace, name="remove"),
    path("config/<str:name>/", views.plugin_config, name="plugin_config")
]