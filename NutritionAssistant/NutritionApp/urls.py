from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("todos", views.todosView, name="todos"),
    path("result", views.search, name="result")
]
