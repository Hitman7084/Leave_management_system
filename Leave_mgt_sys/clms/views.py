from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')