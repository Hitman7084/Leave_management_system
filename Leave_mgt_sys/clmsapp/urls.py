from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # more paths.....
]