import os
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from .models import User, OTPVerification
from .gmail_oauth import send_email_oauth
from .models import LeaveRequest
from .forms import LeaveRequestForm


# Generate OTP
def generate_otp(user):
    otp_instance, created = OTPVerification.objects.get_or_create(user=user)
    otp_instance.generate_otp()
    return otp_instance.otp


# new user registering (Now using OAuth) smtp disable ho gaya :(
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        role = request.POST['role']

        try:
            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email already exists.'})

            # Create new user
            user = User.objects.create_user(username=username, email=email)
            user.full_name = full_name
            user.role = role
            user.is_active = True  # No email verification required
            user.save()

            # Generate and set a random password
            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()

            # Send email using Gmail OAuth
            subject = "Welcome to Leave Management System!"
            message = f"Hello {full_name},\n\nYour account has been created successfully!\n\nYour login credentials:\nUsername: {username}\nPassword: {new_password}\n\nPlease log in and change your password after first login.\n\nBest regards,\nfrom Himanshu"
            send_email_oauth(email, subject, message)

            return JsonResponse({'success': True, 'role': role})
        except IntegrityError:
            return JsonResponse({'success': False, 'error': 'Username already exists.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'register.html')


# Send OTP for pass reset (Now using OAuth) again smtp disabled by google gg
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            otp = get_random_string(length=6)  # Generate a random OTP

            # Send OTP email using OAuth
            subject = "Password Reset Request"
            message = f"Your OTP is {otp}. It is valid for 10 minutes."
            send_email_oauth(email, subject, message)

            messages.success(request, 'OTP sent to your email.')
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')

    return render(request, 'forgot_password.html')


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


# Dashboard Views for Different Roles
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
        return render(request, 'dashboard_default.html')  # Add a default dashboard


@login_required
def dashboard_incharge(request):
    users = User.objects.all()
    return render(request, 'dashboard_incharge.html', {'users': users})



@login_required
def submit_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user
            if leave_request.leave_type == "Emergency":
                leave_request.status = "Forwarded"  # Auto-forward emergency requests to Dean
            leave_request.save()
            return redirect('dashboard_student')  # Redirect after submission
    else:
        form = LeaveRequestForm()
    return render(request, 'submit_leave.html', {'form': form})


@login_required
def incharge_dashboard(request):
    if request.user.groups.filter(name="Incharge").exists():  # keval incahrge dekh paye
        pending_requests = LeaveRequest.objects.filter(status="Pending")
        return render(request, 'dashboard_incharge.html', {'pending_requests': pending_requests})
    return redirect('home')  # Redirect non regstrd users



'''# Test Email Sending (For Debugging OAuth)
def test_email(request):
    try:
        send_email_oauth("testmail@gmail", "Test Email", "This is a test email sent using OAuth!")
        return JsonResponse({'success': True, 'message': 'Test email sent successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})'''
