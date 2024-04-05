from django.urls import path
from . import views



urlpatterns = [
    path('', views.create_task, name = 'create-task'),
    path('<int:id>/', views.get_particular_task_details, name = 'get-single-task'),
    path('update/<int:id>/', views.update_task, name = 'update_task'),
    path('delete/<int:id>/', views.delete_task, name = 'delete_task'),
    path('listAll/', views.list_all_task, name = 'list_all_task'),

    
]
