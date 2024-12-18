
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, staffviews,adminviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    #login Path
    path('', views.FIRSTPAGE, name='firstpage'),
    path('Login', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),

    path('Index', views.INDEX, name='index'),
    #This is Admin Panel
    path('Admin/Home', adminviews.HOME, name='admin_home'),
    path('Admin/Staff/Add',adminviews.ADD_STAFF,name='add_staff'),
    path('Admin/Staff/View',adminviews.VIEW_STAFF,name='view_staff'),
    path('Admin/Staff/Edit/<str:id>',adminviews.EDIT_STAFF,name='edit_staff'),
    path('Admin/Staff/Update',adminviews.UPDATE_STAFF,name='update_staff'),
    path('Admin/Staff/<str:admin>',adminviews.DELETE_STAFF,name='delete_staff'),
    path('Admin/Leaveview',adminviews.STAFF_LEAVE_VIEW,name='staff_leave_view_admin'),
    path('Admin/Leaveview',adminviews.STAFF_LEAVE_VIEW,name='staff_leave_view_admin'),
    path('Admin/Staff/Approve_Leave/<str:id>',adminviews.STAFF_APPROVE_LEAVE,name='staff_approve_leave'),
    path('Admin/Staff/Disapprove_Leave/<str:id>',adminviews.STAFF_DISAPPROVE_LEAVE,name='staff_disapprove_leave'),

    #This is staff panel
    path('Staff/Home', staffviews.HOME, name='staff_home'),
    path('Staff/Apply_Leave', staffviews.STAFF_APPLY_LEAVE, name='staff_apply_leave'),
    path('Staff/Apply_Leave_save', staffviews.STAFF_APPLY_LEAVE_SAVE, name='staff_apply_leave_save'),
    path('Staff/Leaveview',staffviews.STAFF_LEAVE_VIEW,name='staff_leave_view'),
    
    
    #profile path
    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
