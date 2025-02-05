import os
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from django.http import JsonResponse
from .models import User, OTPVerification
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string



# Gen OTP
def generate_otp(user):
    otp_instance, created = OTPVerification.objects.get_or_create(user=user)
    otp_instance.generate_otp()
    return otp_instance.otp

# Send OTP to mail (now generates a new pass)
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()
            send_mail(
                'Account Verification',
                f'Your new password is {new_password}. Please use this to log in.',
                os.getenv('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# Login View (Handles Pass Login)
def login(request):
    role = request.GET.get('role', 'default')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful.')
            return JsonResponse({'success': True, 'role': user.role})
        else:
            messages.error(request, 'Incorrect username or password.')
            return JsonResponse({'success': False, 'error': 'Incorrect username or password.'})

    return render(request, 'login.html', {'role': role})

# Register New User (Sends pass to email)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        role = request.POST['role']

        try:
            # Check if user with the mail already exists in db
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email already exists.'})

            user = User.objects.create_user(username=username, email=email)
            user.full_name = full_name
            user.role = role
            user.is_active = True  # User is active as email verification is not required
            user.save()

            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()

            send_mail(
                'Account Verification',
                f'Your new password is {new_password}. Please use this to log in.',
                os.getenv('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'role': role})
        except IntegrityError:
            return JsonResponse({'success': False, 'error': 'Username already exists.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'register.html')

# Forgot Password (Sends OTP) not applicable yet 
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            otp = generate_otp(user)  # Generate OTP 

            send_mail(
                'Password Reset Request',
                f'Your OTP is {otp}. It is valid for 10 minutes.',
                os.getenv('EMAIL_HOST_USER'),
                [email],
                fail_silently=False,
            )

            messages.success(request, 'OTP sent to your email.')
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'Account not found with this email.')

    return render(request, 'forgot_password.html')

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'Professor':
        return render(request, 'dashboard_prof.html')
    elif user.role == 'Dean':
        return render(request, 'dashboard_dean.html')
    elif user.role == 'Incharge':
        return render(request, 'dashboard_incharge.html')
    elif user.role == 'Student':
        return render(request, 'dashboard_student.html')
    else:
        return render(request, 'dashboard_default.html') # add home maybe idk

''' test_email
def test_email(request):
    email_host_user = os.getenv('EMAIL_HOST_USER')
    email_host_password = os.getenv('EMAIL_HOST_PASSWORD')
    print(f"EMAIL_HOST_USER: {email_host_user}")
    print(f"EMAIL_HOST_PASSWORD: {email_host_password}")

    send_mail(
        'Test Email',
        'This is a test email.',
        email_host_user,
        ['cliad350@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('Email sent successfully.') '''