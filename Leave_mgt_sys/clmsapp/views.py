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
from .models import LeaveApplication
from .forms import LeaveApprovalForm

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

            # Generate & set a random password
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

            # Determine role-based redirection
            role_redirects = {
                'student': 'student_dashboard',
                'professor': 'professor_dashboard',
                'dean': 'dean_dashboard',
                'incharge': 'incharge_dashboard',
            }

            redirect_url = role_redirects.get(user.role, 'home')  # Default redirect if role is unknown

            # Return JSON response for AJAX-based login or redirect if standard form
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Checks if an AJAX request
                return JsonResponse({'success': True, 'role': user.role, 'redirect_url': redirect_url})
            else:
                return redirect(redirect_url)

        else:
            messages.error(request, 'Incorrect username or password.')
            return JsonResponse({'success': False, 'error': 'Incorrect username or password.'})

    return render(request, 'login.html', {'role': role})



@login_required
def student_dashboard(request):
    if request.method == "POST":
        form = LeaveApprovalForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.student = request.user
            leave_request.save()
            return redirect('dashboard_student')
    else:
        form = LeaveApprovalForm()

    incharges = User.objects.filter(role="Incharge")

    return render(request, "dashboard_student.html", {"incharges": incharges, "form": form})


@login_required
def incharge_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(forwarded_to_dean=False)  # Shows only pending requests

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = LeaveApplication.objects.get(id=leave_id)

        if action == "approve":
            leave.incharge_approved = True
            leave.forwarded_to_dean = True  # Forwarded to dean
            leave.rejection_reason = None
        elif action == "reject":
            leave.incharge_approved = False
            leave.forwarded_to_dean = False
            leave.rejection_reason = request.POST.get("rejection_reason")

        leave.save()
        return redirect('dashboard_incharge')

    return render(request, 'dashboard_incharge.html', {'leave_requests': leave_requests})


@login_required
def dean_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(forwarded_to_dean=True)
    return render(request, 'dashboard_dean.html', {'leave_requests': leave_requests})

@login_required
def professor_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(forwarded_to_dean=False)
    return render(request, 'dashboard_professor.html', {'leave_requests': leave_requests})

'''# Test Email Sending (For Debugging OAuth)
def test_email(request):
    try:
        send_email_oauth("testmail@gmail", "Test Email", "This is a test email sent using OAuth!")
        return JsonResponse({'success': True, 'message': 'Test email sent successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})'''
