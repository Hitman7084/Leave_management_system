from django.urls import path
from . import views
from .views import student_dashboard, incharge_dashboard

urlpatterns = [
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/', student_dashboard, name='dashboard_student'),
    path('incharge/', incharge_dashboard, name='dashboard_incharge'),
    # more paths.....
]