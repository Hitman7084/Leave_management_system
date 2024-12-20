from django.shortcuts import render

from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

'''def professor_dashboard(request):
    return render(request, 'professor_dashboard.html')

def incharge_dashboard(request):
    return render(request, 'incharge_dashboard.html')

def dean_dashboard(request):
    return render(request, 'dean_dashboard.html')

def student_dashboard(request):
    return render(request, 'student_dashboard.html')'''

