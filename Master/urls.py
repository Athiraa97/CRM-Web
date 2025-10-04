from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #departments

    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/<str:pk>/edit/', views.department_edit, name='department_edit'),
    path('departments/<str:pk>/', views.department_detail, name='department_detail'),
    path('departments/<str:pk>/delete/', views.department_delete, name='department_delete'),
   
    # Designation
    path('designations/', views.designation_list, name='designation_list'),
    path('designations/add/', views.designation_add, name='designation_add'),
    path('designations/<str:pk>/edit/', views.designation_edit, name='designation_edit'),
    path('designations/<str:pk>/', views.designation_detail, name='designation_detail'),
    path('designations/<str:pk>/delete/', views.designation_delete, name='designation_delete'),

    #Location
    path('locations/', views.location_list, name='location_list'),
    path('locations/add/', views.location_add, name='location_add'),
    path('locations/<str:pk>/edit/', views.location_edit, name='location_edit'),
    path('locations/<str:pk>/', views.location_detail, name='location_detail'),
    path('locations/<str:pk>/delete/', views.location_delete, name='location_delete'),





]




