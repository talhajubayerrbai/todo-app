from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('todos/create/', views.todo_create, name='todo-create'),
    path('todos/<int:pk>/toggle/', views.todo_toggle, name='todo-toggle'),
    path('todos/<int:pk>/delete/', views.todo_delete, name='todo-delete'),
    path('health/', views.health, name='health'),
]
