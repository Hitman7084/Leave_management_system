from django.urls import path
from . import views
from .views import student_dashboard, dean_dashboard, incharge_dashboard, professor_dashboard

urlpatterns = [
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/', views.login, name='login'),
    path('student/', student_dashboard, name='dashboard_student'),
    path('incharge/', incharge_dashboard, name='dashboard_incharge'),
    path('dean/', dean_dashboard, name='dashboard_dean'),
    path('professor/', views.professor_dashboard, name='dashboard_professor'),
    # more paths.....
]