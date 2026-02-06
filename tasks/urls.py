from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.task_list, name='task_list'),

    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]