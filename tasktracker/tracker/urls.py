from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
]
