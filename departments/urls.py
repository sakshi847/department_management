from django.urls import path
from . import views

urlpatterns = [
    path('', views.department_list, name='department_list'),
    path('create/', views.department_create, name='department_create'),
    path('update/<int:dept_id>/', views.department_update, name='department_update'),
    path('delete/<int:dept_id>/', views.department_delete, name='department_delete'),
]


