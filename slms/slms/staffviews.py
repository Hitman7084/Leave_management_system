from django.shortcuts import render,redirect,HttpResponse
from slmsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from slmsapp.models import CustomUser,Staff,Staff_Leave
from django.db.models import Q




@login_required(login_url='/')
def HOME(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_Leave.objects.filter(staff_id = staff_id)
        context = {
            'staff_leave_history':staff_leave_history,
        }
    

    return render(request,'staff/home.html',context)

@login_required(login_url='/')   
def STAFF_APPLY_LEAVE(request):
    return render(request,'staff/apply_leave.html')


@login_required(login_url='/')   
def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_type = request.POST.get('leave_type')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = request.user.id)

        leave = Staff_Leave(
            staff_id = staff,
            leave_type = leave_type,
            from_date = from_date,
            to_date = to_date,
            message = message,


          )
        leave.save()
        messages.success(request,'Leave apply successfully')
        return redirect('staff_apply_leave')

@login_required(login_url='/')    
def STAFF_LEAVE_VIEW(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_Leave.objects.filter(staff_id = staff_id)
        context = {
            'staff_leave_history':staff_leave_history,
        }
        return render(request,'staff/leave_history.html',context)