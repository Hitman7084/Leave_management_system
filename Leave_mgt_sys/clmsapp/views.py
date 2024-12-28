from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import RegistrationForm, ForgotPasswordForm
from .models import User
import random

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False                # Account not created until verification is done
            user.save()

            # Otp generation
            otp = random.randint(10000, 99999)
            request.session['otp'] = otp
            request.session['email'] = user.email

            send_mail(
                'Account Verification',
                f'Your OTP is {otp}. It is valid for 5 minutes.',
                'cliad525@gmail.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Account created successfully. Please verify your email.')
            return redirect('verify_email')
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    
def verify_email(request):
    if request.method == 'POST':
        otp = request.POST.get['otp']
        if str(otp) == str(request.session.get('otp')):
            email = request.session.get('email')
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(request, 'Account verified successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP.')
    return render(request, 'verify_email.html')
    
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                reset_token = random.randint(10000, 99999)
                request.session['reset_token'] = reset_token
                request.session['email'] = email

                send_mail(
                    'Password Reset Request',
                    f'Your OTP is {reset_token}. It is valid for 5 minutes.',
                    'cliad350@gmail.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent to your email.')
                return redirect('reset_password')
            except User.DoesNotExist:
                messages.error(request, 'Account not found with this email.')
        else:
            form = ForgotPasswordForm()
        return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        reset_token = request.POST.get['reset_token']
        new_password = request.POST.get['new_password']
        confirm_password = request.POST.get['confirm_password']
        if str(reset_token) == str(request.session.get('reset_token')):
            email = request.session.get('email')
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfull.')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match.')
    else:
        messages.error(request, 'Invalid OTP.')
    return render(request, 'reset_password.html')

