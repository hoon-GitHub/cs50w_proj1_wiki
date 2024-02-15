from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page")
]
