from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from .forms import RegistrationForm, ForgotPasswordForm
from .models import User, OTPVerification
import random

# ✅ Secure OTP generation function
def generate_otp(user):
    otp, created = OTPVerification.objects.get_or_create(user=user)
    otp.otp = str(random.randint(10000, 99999))  # Generate 5-digit OTP
    otp.expires_at = timezone.now() + timezone.timedelta(minutes=5)  # Set expiry time
    otp.verified = False
    otp.save()
    return otp.otp

# ✅ Register New User (Sends OTP for Email Verification)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until email is verified
            user.save()

            otp = generate_otp(user)  # Secure OTP storage

            send_mail(
                'Account Verification',
                f'Your OTP is {otp}. It is valid for 5 minutes.',
                'your-email@gmail.com',  # Use environment variables in production
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Account created successfully. Please verify your email.')
            return redirect('verify_email')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# ✅ Verify Email OTP
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
                messages.success(request, 'Account verified successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid or Expired OTP.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'verify_email.html')

# ✅ Forgot Password (Sends OTP)
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
                otp = generate_otp(user)  # Generate OTP securely

                send_mail(
                    'Password Reset Request',
                    f'Your OTP is {otp}. It is valid for 5 minutes.',
                    'your-email@gmail.com',
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

# ✅ Reset Password (Verifies OTP)
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
