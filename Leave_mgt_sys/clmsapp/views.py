import os
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from django.http import JsonResponse
from .models import User, OTPVerification
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse



# Gen OTP
def generate_otp(user):
    otp_instance, created = OTPVerification.objects.get_or_create(user=user)
    otp_instance.generate_otp()
    return otp_instance.otp

# Send OTP to mail
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = generate_otp(user)
            send_mail(
                'Account Verification',
                f'Your OTP is {otp}. It is valid for 10 minutes.',
                os.getenv('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# Login View (Handles OTP Login)
def login(request):
    role = request.GET.get('role', 'default')
    if request.method == 'POST':
        username = request.POST['username']
        otp = request.POST['otp']
        role = request.POST.get('role')

        try:
            user = User.objects.get(username=username)
            otp_instance = OTPVerification.objects.filter(user=user, verified=False).first()

            if otp_instance and str(otp_instance.otp) == str(otp) and otp_instance.expires_at > timezone.now():
                otp_instance.verified = True
                otp_instance.save()
                user.is_active = True
                user.save()
                messages.success(request, 'Login successful.')

                if role == 'Professor':
                    return redirect('dashboard_prof')
                elif role == 'Dean':
                    return redirect('dashboard_dean')
                elif role == 'Incharge':
                    return redirect('dashboard_incharge')
                elif role == 'Student':
                    return redirect('dashboard_student')
                else:
                    return redirect('dashboard_default')
            else:
                messages.error(request, 'Invalid or Expired OTP.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'login.html', {'role': role})

# Register New User (Sends OTP for mail Verifs)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        role = request.POST['role']

        try:
            user = User.objects.create_user(username=username, email=email)
            user.full_name = full_name
            user.role = role
            user.is_active = False  # User is inactive until email verification
            user.save()

            otp = generate_otp(user)  

            send_mail(
                'Account Verification',
                f'Your OTP is {otp}. It is valid for 10 minutes.',
                os.getenv('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False,
            )

            return redirect(f"{reverse('login')}?role={role}")
        except IntegrityError:
            return JsonResponse({'success': False, 'error': 'Username already exists.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'register.html')

# Verify Email OTP
def verify_email(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            otp_instance = OTPVerification.objects.filter(user=user, verified=False).first()

            if otp_instance and str(otp_instance.otp) == str(otp) and otp_instance.expires_at > timezone.now():
                otp_instance.verified = True
                otp_instance.save()
                user.is_active = True
                user.save()
                messages.success(request, 'Account verification successful.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid or Expired OTP.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'verify_email.html')

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

# Reset Password (Verifies OTP) not applicable yet as well
def reset_password(request):
    if request.method == 'POST':
        otp = request.POST.get('reset_token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        try:
            user = User.objects.get(email=email)
            otp_instance = OTPVerification.objects.filter(user=user, verified=False).first()

            if otp_instance and str(otp_instance.otp) == str(otp) and otp_instance.expires_at > timezone.now():
                user.set_password(new_password)
                user.save()
                otp_instance.verified = True  # Mark OTP as used
                otp_instance.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid or Expired OTP.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'reset_password.html')

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