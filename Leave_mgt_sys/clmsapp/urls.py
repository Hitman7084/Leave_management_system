from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_incharge/', views.dashboard_incharge, name='dashboard_incharge'),
    # more paths.....
]