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
                'cliad350@gmail.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Account created successfully. Please verify your email.')
            return redirect('verify_email')
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})