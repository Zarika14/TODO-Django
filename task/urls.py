from django.urls import path
from . import views



urlpatterns = [
    path('', views.create_task, name = 'create-task'),
    path('/<str:id>/', views.get_particular_task_details, name = 'get-single-task')
   
]
