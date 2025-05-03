from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/', views.login, name='login'),
    path('student/', views.student_dashboard, name='dashboard_student'),
    path('incharge/', views.incharge_dashboard, name='dashboard_incharge'),
    path('dean/', views.dean_dashboard, name='dashboard_dean'),
    path('professor/', views.professor_dashboard, name='dashboard_professor'),
    path('student_form/', views.student_form, name='student_form'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('student_history/', views.student_history, name='student_history'),
    path('incharge_history/', views.incharge_history, name='incharge_history'),
    # more paths.....
]