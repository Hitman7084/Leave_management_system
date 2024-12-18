from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import  logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from clmsapp.models import CustomUser
from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()

def BASE(request):
    return render(request,'base.html')

def FIRSTPAGE(request):
    return render(request,'firstpage.html')