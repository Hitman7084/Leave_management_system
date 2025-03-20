from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_incharge/', views.dashboard_incharge, name='dashboard_incharge'),
    path('submit-leave-ajax/', views.submit_leave_request_ajax, name='submit_leave_ajax'),
    path('incharge/', views.incharge_dashboard, name='dashboard_incharge'),
    path('incharge/<int:leave_id>/<str:action>/', views.process_leave_incharge, name='process_leave_incharge'),
    path('dean/', views.dean_dashboard, name='dashboard_dean'),
    path('dean/<int:leave_id>/<str:action>/', views.process_leave_dean, name='process_leave_dean'),
    # more paths.....
]