from django.shortcuts import render

from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authentication logic lagana hai yha
        if username == 'admin' and password == 'aspirin':  # Example 
            return render(request, 'authenticate_user.html', {
                'authenticated': True,
                'username': username,
            })
    return render(request, 'authenticate_user.html', {'authenticated': False})

'''def professor_dashboard(request):
    return render(request, 'professor_dashboard.html')

def incharge_dashboard(request):
    return render(request, 'incharge_dashboard.html')

def dean_dashboard(request):
    return render(request, 'dean_dashboard.html')

def student_dashboard(request):
    return render(request, 'student_dashboard.html')'''

