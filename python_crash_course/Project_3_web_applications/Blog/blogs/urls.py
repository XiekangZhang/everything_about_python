from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add_blog/", views.add_blog, name="add_blog"),
    path("edit_blog/<int:blog_id>/", views.edit_blog, name="edit_blog")
]