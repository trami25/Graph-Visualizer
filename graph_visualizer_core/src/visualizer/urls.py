from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:tag>/", views.workspace, name="workspace"),
]