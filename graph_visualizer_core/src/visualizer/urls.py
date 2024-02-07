from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("workspace/<str:tag>/", views.workspace_view, name="workspace"),
    path("new/", views.new_workspace, name="new"),
    path("remove/", views.remove_workspace, name="remove")
]