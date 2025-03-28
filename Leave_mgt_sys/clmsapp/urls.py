from django.urls import path
from . import views
from .views import login, student_dashboard, professor_dashboard, dean_dashboard, incharge_dashboard

urlpatterns = [
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/', views.login, name='login'),
    path('student/', student_dashboard, name='student_dashboard'),
    path('professor/', professor_dashboard, name='professor_dashboard'),
    path('dean/', dean_dashboard, name='dean_dashboard'),
    path('incharge/', incharge_dashboard, name='incharge_dashboard'),  # Ensure this line exists
    # more paths.....
]