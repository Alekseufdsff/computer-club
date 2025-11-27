from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('computers/', views.computers_list, name='computers_list'),
    path('computers/<int:computer_id>/', views.computer_detail, name='computer_detail'),
    path('computers/<int:computer_id>/request/', views.request_computer, name='request_computer'),
    
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/computers/', views.admin_computers, name='admin_computers'),
    path('admin/news/', views.admin_news, name='admin_news'),
    path('admin/tariffs/', views.admin_tariffs, name='admin_tariffs'),
    path('admin/interns/', views.admin_interns, name='admin_interns'),
    path('admin/process_request/<int:request_id>/', views.process_request, name='process_request'),
]