from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/', views.login, name='login'),
    path("dashboard/", dashboard, name="dashboard"),  # Ensure this line exists
    # more paths.....
]