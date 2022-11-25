"""Defines URL patterns for learning_logs"""

from django.urls import path
from . import views

app_name = "learning_logs"
urlpatterns = [
    # Home page
    path("", views.index, name="index"),  # INFO: later we could use this name instead of the whole link
    path("topics/", views.topics, name="topics"),
]
