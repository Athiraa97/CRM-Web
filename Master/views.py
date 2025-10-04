from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseServerError
from . import database_query as dbq
from .models import *
from .forms import *
import traceback  # helpful for debugging unexpected errors


def login_view(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(f"Attempting login for: {username}")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(f"Authenticated: {user.username}")
                auth_login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                print("Invalid credentials")
                messages.error(request, "Invalid username or password.")
    except Exception as e:
        print("Error during login:")
        traceback.print_exc()
        messages.error(request, f"Something went wrong: {str(e)}")

    return render(request, 'login.html')


def logout_view(request):
    try:
        auth_logout(request)
        print("User logged out successfully")
    except Exception as e:
        print("Error during logout:")
        traceback.print_exc()
        messages.error(request, f"Logout failed: {str(e)}")

    return redirect('login')


@login_required
def dashboard(request):
    try:
        username = request.user.username
        print(f"Logged-in user: {username}")
        context = {'username': username}
        return render(request, 'index.html', context)
    except Exception as e:
        print("Error loading dashboard:")
        traceback.print_exc()
        messages.error(request, f"Failed to load dashboard: {str(e)}")
        return HttpResponseServerError("Internal Server Error")
    
#*****************  Master *********************
# ---------------- Department CRUD ----------------
@login_required
def department_list(request):
    username = request.user.username
    departments = dbq.get_departments()   # raw SQL retrieval
    return render(request, 'master/department_list.html', {'username': username,'departments': departments})

@login_required
def department_add(request):
    username = request.user.username
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save(commit=False)
            user = request.user.username
            dept.created_by = user
            dept.updated_by = user
            dept.save()
            messages.success(request, "Department added.")
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'master/department_form.html', {'form': form, 'action': 'Add','username':username})

@login_required
def department_edit(request, pk):
    username = request.user.username
    dept = get_object_or_404(Department, department_id=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user.username
            obj.save()
            messages.success(request, "Department updated.")
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'master/department_form.html', {'form': form, 'action': 'Edit','username':username})

@login_required
def department_detail(request, pk):
    username = request.user.username
    dept = get_object_or_404(Department, department_id=pk)
    return render(request, 'master/department_detail.html', {'dept': dept,'username':username})

@login_required
def department_delete(request, pk):
    username = request.user.username
    dept = get_object_or_404(Department, department_id=pk)
    if dbq.is_department_used(pk):
        messages.error(request, "Cannot delete department because it is used by other records.")
        return redirect('department_list')
    if request.method == 'POST':
        dept.delete()
        messages.success(request, "Department deleted.")
        return redirect('department_list')
    return render(request, 'master/department_detail.html', {'dept': dept, 'confirm_delete': True,'username':username})

# ---------------- Location CRUD ------
# ---------------- Designation CRUD ----------------
@login_required
def designation_list(request):
    username = request.user.username
    designations = dbq.get_designations()
    return render(request, 'master/designation_list.html', {'designations': designations,'username':username})

@login_required
def designation_add(request):
    username = request.user.username
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            des = form.save(commit=False)
            des.created_by = request.user.username
            des.updated_by = request.user.username
            des.save()
            messages.success(request, "Designation added.")
            return redirect('designation_list')
    else:
        form = DesignationForm()
    return render(request, 'master/designation_form.html', {'form': form, 'action': 'Add','username':username})

@login_required
def designation_edit(request, pk):
    username = request.user.username
    des = get_object_or_404(Designation, designation_id=pk)
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=des)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user.username
            obj.save()
            messages.success(request, "Designation updated.")
            return redirect('designation_list')
    else:
        form = DesignationForm(instance=des)
    return render(request, 'master/designation_form.html', {'form': form, 'action': 'Edit','username':username})

@login_required
def designation_detail(request, pk):
    username = request.user.username
    des = get_object_or_404(Designation, designation_id=pk)
    return render(request, 'master/designation_detail.html', {'des': des,'username':username})

@login_required
def designation_delete(request, pk):
    username = request.user.username
    des = get_object_or_404(Designation, designation_id=pk)
    if dbq.is_designation_used(pk):
        messages.error(request, "Cannot delete designation because it is used by other records.")
        return redirect('designation_list')
    if request.method == 'POST':
        des.delete()
        messages.success(request, "Designation deleted.")
        return redirect('designation_list')
    return render(request, 'master/designation_detail.html', {'des': des, 'confirm_delete': True,'username':username})


# ---------------- Location CRUD ----------------
@login_required
def location_list(request):
    username = request.user.username
    locations = dbq.get_locations()
    return render(request, 'master/location_list.html', {'locations': locations,'username':username})

@login_required
def location_add(request):
    username = request.user.username
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            loc = form.save(commit=False)
            loc.created_by = request.user.username
            loc.updated_by = request.user.username
            loc.save()
            messages.success(request, "Location added.")
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'master/location_form.html', {'form': form, 'action': 'Add','username':username})

@login_required
def location_edit(request, pk):
    username = request.user.username
    loc = get_object_or_404(Location, location_id=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=loc)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user.username
            obj.save()
            messages.success(request, "Location updated.")
            return redirect('location_list')
    else:
        form = LocationForm(instance=loc)
    return render(request, 'master/location_form.html', {'form': form, 'action': 'Edit','username':username})

@login_required
def location_detail(request, pk):
    username = request.user.username
    loc = get_object_or_404(Location, location_id=pk)
    return render(request, 'master/location_detail.html', {'loc': loc,'username':username})

@login_required
def location_delete(request, pk):
    username = request.user.username
    loc = get_object_or_404(Location, location_id=pk)
    if dbq.is_location_used(pk):
        messages.error(request, "Cannot delete location because it is used by other records.")
        return redirect('location_list')
    if request.method == 'POST':
        loc.delete()
        messages.success(request, "Location deleted.")
        return redirect('location_list')
    return render(request, 'master/location_detail.html', {'loc': loc, 'confirm_delete': True,'username':username})
