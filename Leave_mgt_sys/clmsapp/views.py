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
from datetime import datetime, timedelta

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
            # Check if email already exists
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
            message = f"Hello {full_name},\n\nYour account has been created successfully!\n\nYour login credentials:\nUsername: {username}\nPassword: {new_password}\nRole: {role}\n\nPlease log in and change your password after first login.\n\nBest regards,\nfrom Himanshu"
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

            # Return JSON response for AJAX based login or redirects if std form
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
    return render(request, 'dashboard_student.html')


@login_required
def incharge_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(status="Pending")

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")

        try:
            leave = LeaveApplication.objects.get(id=leave_id)
        except LeaveApplication.DoesNotExist:
            messages.error(request, "Leave request not found!")
            return redirect('dashboard_incharge')

        if action == "approve":
            leave.incharge_approved = True
            leave.forwarded_to_dean = True
            leave.status = "Forwarded to Dean"
            leave.rejection_reason = None
        elif action == "reject":
            leave.incharge_approved = False
            leave.forwarded_to_dean = False
            leave.status = "Rejected by Incharge"
            leave.rejection_reason = request.POST.get("rejection_reason")

        leave.save()
        return redirect('dashboard_incharge') 

    return render(request, 'dashboard_incharge.html', {'leave_requests': leave_requests})

def incharge_history(request):
    leave_requests = LeaveApplication.objects.filter(incharge=request.user).order_by("-submitted_at")
    return render(request, 'incharge_history.html', {'leave_requests': leave_requests})

@login_required
def dean_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(forwarded_to_dean=True)
    return render(request, 'dashboard_dean.html', {'leave_requests': leave_requests})

@login_required
def professor_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(forwarded_to_dean=False)
    return render(request, 'dashboard_professor.html', {'leave_requests': leave_requests})

def student_form(request):
    incharges = User.objects.filter(role="Incharge")

    if request.method == "POST":
        student = request.user
        recipient_id = request.POST.get("recipient")
        leave_type = request.POST.get("leave_type")  # Get leave type from form
        message = request.POST.get("message")
        attachment = request.FILES.get("attachment")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if not recipient_id or not message or not start_date or not end_date or not leave_type:
            messages.error(request, "Please fill in all required fields.")
            return redirect("student_form")

        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            messages.error(request, "Selected incharge does not exist.")
            return redirect("student_form")

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect("student_form")

        if start_date > end_date:
            messages.error(request, "Start date cannot be after end date.")
            return redirect("student_form")

        leave_request = LeaveApplication.objects.create(
            student=student,
            incharge=recipient,
            leave_type=leave_type,  # Include leave type
            message=message,
            attachment=attachment,
            start_date=start_date,
            end_date=end_date,
            status="Pending"
        )

        messages.success(request, "Leave request submitted successfully.")
        return redirect("student_form")

    return render(request, "student_form.html", {"incharges": incharges})

def student_profile(request):
    return render(request, 'student_profile.html')

def student_history(request):
    leave_requests = LeaveApplication.objects.filter(student=request.user).order_by("-submitted_at")
    return render(request, 'student_history.html', {'leave_requests': leave_requests})

def leave_calendar_api(request):
    leaves = LeaveApplication.objects.all()
    events = []

    leave_colors = {
        "casual": "#3498db",     # Blue
        "duty": "#2ecc71",       # Green
        "medical": "#e74c3c",    # Red
        "emergency": "#f1c40f"   # Yellow
    }

    for leave in leaves:
        if leave.start_date and leave.end_date:
            events.append({
                "title": f"{leave.student.full_name} ({leave.get_leave_type_display()})",
                "start": leave.start_date.strftime("%Y-%m-%d"),
                "end": leave.end_date.strftime("%Y-%m-%d"),
                "color": leave_colors.get(leave.leave_type, "#3788d8"),
            })

    return JsonResponse(events, safe=False)


'''# Test Email Sending (For Debugging OAuth)
def test_email(request):
    try:
        send_email_oauth("testmail@gmail", "Test Email", "This is a test email sent using OAuth!")
        return JsonResponse({'success': True, 'message': 'Test email sent successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})'''
