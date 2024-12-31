from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
]
