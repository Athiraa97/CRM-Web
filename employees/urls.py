from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_add, name='employee_add'),
    path('edit/<str:pk>/', views.employee_edit, name='employee_edit'),
    path('detail/<str:pk>/', views.employee_detail, name='employee_detail'),
    path('delete/<str:pk>/', views.employee_delete, name='employee_delete'),
    path('ajax/locations/', views.ajax_locations, name='ajax_locations'),
    path('ajax/designations/', views.ajax_designations, name='ajax_designations'),
    path('download_selected/', views.download_selected, name='download_selected'),
]
