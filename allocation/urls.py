from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='allocation/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # Admin pages
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('students/', views.student_list, name='student_list'),
    path('allocations/', views.allocation_list, name='allocation_list'),
    path('allocations/add/', views.allocation_add, name='allocation_add'),
    path('allocations/<int:pk>/vacate/', views.allocation_vacate, name='allocation_vacate'),
    path('waitlist/', views.waitlist, name='waitlist'),
    path('waitlist/add/', views.waitlist_add, name='waitlist_add'),
    path('waitlist/<int:pk>/remove/', views.waitlist_remove, name='waitlist_remove'),
    path('ajax/load-rooms/',views.load_rooms,name='ajax_load_rooms'),

    # Student page
    path('my-room/', views.student_dashboard, name='student_dashboard'),
    path('apply/', views.apply_for_room, name='apply_for_room'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin-login/', views.admin_login, name='admin_login'),
    
    # Fees
    path('fees/', views.fee_list, name='fee_list'),
    path('fees/add/', views.fee_add, name='fee_add'),
    path('fees/<int:pk>/toggle/', views.fee_toggle, name='fee_toggle'),
    path('my-fees/', views.my_fees, name='my_fees'),
]