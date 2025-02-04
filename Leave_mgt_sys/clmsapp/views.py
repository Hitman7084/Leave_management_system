import os
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from .models import User, OTPVerification
import random

# Generate OTP
def generate_otp(user):
    otp_instance, created = OTPVerification.objects.get_or_create(user=user)
    otp_instance.generate_otp()
    return otp_instance.otp

# Register New User (Sends OTP for Email Verification)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        photo = request.FILES.get('photo')
        role = request.POST['role']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.full_name = full_name
            user.photo = photo
            user.role = role
            user.is_active = False  # User is inactive until email verification
            user.save()

            otp = generate_otp(user)  

            send_mail(
                'Account Verification',
                f'Your OTP is {otp}. It is valid for 10 minutes.',
                os.getenv('EMAIL_HOST_USER'),  # env variables usage here
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Account created successfully. Please verify your email.')
            return redirect('verify_email')
        except IntegrityError:
            messages.error(request, 'Username already exists.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

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

# Forgot Password (Sends OTP)
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

# Reset Password (Verifies OTP)
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