from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard:home'), name='logout'),
    
    path('', views.home, name='home'),

    # Portal landing page first
    path('portal/', views.portal_landing, name='portal_landing'),
    path('portal/<str:page_key>/', views.portal_page, name='portal_page'),

    # Authentication URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('portal/courses/', views.portal_courses, name='portal_courses'),
    path('portal/grades/', views.portal_grades, name='portal_grades'),
    path('portal/finance/', views.portal_finance, name='portal_finance'),
    path('portal/library/', views.library_page, name='library_page'),
    path('portal/events/', views.events_page, name='events_page'),
    path('profile/', views.profile_view, name='profile'),
    path('help/', views.help_page, name='help_page'),
    path('register/', views.register, name='register'),
    path("<str:page_key/", views.portal_page, name="portal_page"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
]