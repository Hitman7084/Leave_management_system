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
from .models import LeaveApplication, LeaveBalance
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
    balance, created = LeaveBalance.objects.get_or_create(student=request.user)

    leave_data = {
        'casual': balance.casual,
        'duty': balance.duty,
        'medical': balance.medical,
        'emergency': balance.emergency
    }

    return render(request, 'dashboard_student.html', {
        'leave_data': leave_data
    })


@login_required
def incharge_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(status="Pending")

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")

        print(f"POST received: leave_id={leave_id}, action={action}")  # Debug print

        try:
            leave = LeaveApplication.objects.get(id=leave_id)
        except LeaveApplication.DoesNotExist:
            messages.error(request, "Leave request not found!")
            return redirect('dashboard_incharge')

        if action == "forward":
            leave.status = "Forwarded to Dean"
            leave.rejection_reason = None  # reset original rejection reason diya gaya by incharge
            leave.approval_note = f"Approved by {request.user.full_name or request.user.username}"
            leave.save()
            messages.success(request, "Leave forwarded to Dean.")
        elif action == "reject":
            leave.status = "Rejected by Incharge"
            leave.rejection_reason = request.POST.get("rejection_reason")
            messages.success(request, "Leave rejected.")

        leave.save()  
        return redirect('dashboard_incharge')

    return render(request, 'dashboard_incharge.html', {'leave_requests': leave_requests})

@login_required
def incharge_history(request):
    leave_requests = LeaveApplication.objects.filter(incharge=request.user).order_by("-submitted_at")
    return render(request, 'incharge_history.html', {'leave_requests': leave_requests})

@login_required
def dean_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(status="Forwarded to Dean")

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")

        try:
            leave = LeaveApplication.objects.get(id=leave_id)
        except LeaveApplication.DoesNotExist:
            messages.error(request, "Leave request not found!")
            return redirect('dashboard_dean')

        if action == "approve":
            leave.status = "Approved"
            leave.rejection_reason = None
            leave.approval_note = f"Approved by Dean {request.user.full_name or request.user.username}"
            leave.save()

            days = (leave.end_date - leave.start_date).days + 1
            balance, created = LeaveBalance.objects.get_or_create(student=leave.student)
            balance.deduct(leave.leave_type, days)
        elif action == "reject":
            leave.status = "Rejected by Dean"
            leave.rejection_reason = request.POST.get("rejection_reason")
            messages.success(request, "Leave rejected.")

        leave.save()
        return redirect('dashboard_dean')

    return render(request, 'dashboard_dean.html', {'leave_requests': leave_requests})

@login_required
def dean_history(request):
    # Get all leave requests that have been processed by the dean (either approved or rejected)
    leave_requests = LeaveApplication.objects.filter(status__in=["Approved", "Rejected by Dean"]).order_by("-submitted_at")
    return render(request, 'dean_history.html', {'leave_requests': leave_requests})

@login_required
def professor_dashboard(request):
    leave_requests = LeaveApplication.objects.filter(forwarded_to_dean=False)
    return render(request, 'dashboard_professor.html', {'leave_requests': leave_requests})

@login_required
def student_form(request):
    incharges = User.objects.filter(role="Incharge")

    if request.method == "POST":
        student = request.user
        recipient_id = request.POST.get("recipient")
        leave_type = request.POST.get("leave_type")
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

        # Leave balance validation
        try:
            balance = LeaveBalance.objects.get(student=student)
        except LeaveBalance.DoesNotExist:
            messages.error(request, "Leave balance not found.")
            return redirect("student_form")

        total_days = (end_date - start_date).days + 1
        available_days = getattr(balance, leave_type, 0)

        if total_days > available_days:
            messages.error(request, f"Insufficient {leave_type} leave balance. You have {available_days} day(s) left.")
            return redirect("student_form")

        # All good, save application
        LeaveApplication.objects.create(
            student=student,
            incharge=recipient,
            leave_type=leave_type,
            message=message,
            attachment=attachment,
            start_date=start_date,
            end_date=end_date,
            status="Pending"
        )

        messages.success(request, "Leave request submitted successfully.")
        return redirect("student_form")

    return render(request, "student_form.html", {"incharges": incharges})

@login_required
def student_profile(request):
    return render(request, 'student_profile.html')

@login_required
def student_history(request):
    leave_requests = LeaveApplication.objects.filter(student=request.user).order_by("-submitted_at")
    return render(request, 'student_history.html', {'leave_requests': leave_requests})



'''# Test Email Sending (For Debugging OAuth)
def test_email(request):
    try:
        send_email_oauth("testmail@gmail", "Test Email", "This is a test email sent using OAuth!")
        return JsonResponse({'success': True, 'message': 'Test email sent successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})'''
