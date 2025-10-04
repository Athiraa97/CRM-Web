from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.db import DatabaseError
from . import database_query as dbq
from .models import *
from .forms import *


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
        messages.error(request, f"Failed to load dashboard: {str(e)}")
        return HttpResponseServerError("Internal Server Error")
    
#*****************  Master *********************
# ---------------- Department  ----------------

@login_required
def department_list(request):
    username = request.user.username
    try:
        departments = dbq.get_departments()
    except DatabaseError as e:
        messages.error(request, f"Error loading departments: {e}")
        departments = []
    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        departments = []
    return render(request, 'master/department_list.html', {
        'username': username,
        'departments': departments
    })


@login_required
def department_add(request):
    username = request.user.username
    try:
        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                dept = form.save(commit=False)
                dept.created_by = username
                dept.updated_by = username
                dept.save()
                messages.success(request, "Department added successfully.")
                return redirect('department_list')
        else:
            form = DepartmentForm()
    except DatabaseError as e:
        messages.error(request, f"Database error while adding department: {e}")
        form = DepartmentForm()
    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        form = DepartmentForm()

    return render(request, 'master/department_form.html', {
        'form': form,
        'action': 'Add',
        'username': username
    })


@login_required
def department_edit(request, pk):
    username = request.user.username
    try:
        dept = get_object_or_404(Department, department_id=pk)
        if request.method == 'POST':
            form = DepartmentForm(request.POST, instance=dept)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.updated_by = username
                obj.save()
                messages.success(request, "Department updated successfully.")
                return redirect('department_list')
        else:
            form = DepartmentForm(instance=dept)
    except DatabaseError as e:
        messages.error(request, f"Database error while updating department: {e}")
        form = DepartmentForm()
    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        form = DepartmentForm()

    return render(request, 'master/department_form.html', {
        'form': form,
        'action': 'Edit',
        'username': username
    })


@login_required
def department_detail(request, pk):
    username = request.user.username
    try:
        dept = get_object_or_404(Department, department_id=pk)
    except Exception as e:
        messages.error(request, f"Error loading department details: {e}")
        return redirect('department_list')

    return render(request, 'master/department_detail.html', {
        'dept': dept,
        'username': username
    })


@login_required
def department_delete(request, pk):
    username = request.user.username
    try:
        dept = get_object_or_404(Department, department_id=pk)

        if dbq.is_department_used(pk):
            messages.warning(request, "Cannot delete department — it is used by other records.")
            return redirect('department_list')

        if request.method == 'POST':
            dept.delete()
            messages.success(request, "Department deleted successfully.")
            return redirect('department_list')
    except DatabaseError as e:
        messages.error(request, f"Database error while deleting department: {e}")
        return redirect('department_list')
    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        return redirect('department_list')

    return render(request, 'master/department_detail.html', {
        'dept': dept,
        'confirm_delete': True,
        'username': username
    })

# ---------------- Designation  ----------------

@login_required
def designation_list(request):
    username = request.user.username
    try:
        designations = dbq.get_designations()
    except DatabaseError as e:
        messages.error(request, f"Error loading designations: {e}")
        designations = []
    return render(request, 'master/designation_list.html', {'designations': designations, 'username': username})


@login_required
def designation_add(request):
    username = request.user.username
    try:
        if request.method == 'POST':
            form = DesignationForm(request.POST)
            if form.is_valid():
                des = form.save(commit=False)
                des.created_by = username
                des.updated_by = username
                des.save()
                messages.success(request, "Designation added successfully.")
                return redirect('designation_list')
        else:
            form = DesignationForm()
    except Exception as e:
        messages.error(request, f"Error adding designation: {e}")
        form = DesignationForm()
    return render(request, 'master/designation_form.html', {'form': form, 'action': 'Add', 'username': username})


@login_required
def designation_edit(request, pk):
    username = request.user.username
    try:
        des = get_object_or_404(Designation, designation_id=pk)
        if request.method == 'POST':
            form = DesignationForm(request.POST, instance=des)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.updated_by = username
                obj.save()
                messages.success(request, "Designation updated successfully.")
                return redirect('designation_list')
        else:
            form = DesignationForm(instance=des)
    except Exception as e:
        messages.error(request, f"Error updating designation: {e}")
        form = DesignationForm()
    return render(request, 'master/designation_form.html', {'form': form, 'action': 'Edit', 'username': username})


@login_required
def designation_detail(request, pk):
    username = request.user.username
    try:
        des = get_object_or_404(Designation, designation_id=pk)
    except Exception as e:
        messages.error(request, f"Error loading designation details: {e}")
        return redirect('designation_list')
    return render(request, 'master/designation_detail.html', {'des': des, 'username': username})


@login_required
def designation_delete(request, pk):
    username = request.user.username
    try:
        des = get_object_or_404(Designation, designation_id=pk)
        if dbq.is_designation_used(pk):
            messages.warning(request, "Cannot delete — designation is used by other records.")
            return redirect('designation_list')

        if request.method == 'POST':
            des.delete()
            messages.success(request, "Designation deleted successfully.")
            return redirect('designation_list')
    except Exception as e:
        messages.error(request, f"Error deleting designation: {e}")
        return redirect('designation_list')

    return render(request, 'master/designation_detail.html', {'des': des, 'confirm_delete': True, 'username': username})

# ---------------- Location  ----------------
@login_required
def location_list(request):
    username = request.user.username
    try:
        locations = dbq.get_locations()
    except DatabaseError as e:
        messages.error(request, f"Error loading locations: {e}")
        locations = []
    return render(request, 'master/location_list.html', {'locations': locations, 'username': username})


@login_required
def location_add(request):
    username = request.user.username
    try:
        if request.method == 'POST':
            form = LocationForm(request.POST)
            if form.is_valid():
                loc = form.save(commit=False)
                loc.created_by = username
                loc.updated_by = username
                loc.save()
                messages.success(request, "Location added successfully.")
                return redirect('location_list')
        else:
            form = LocationForm()
    except Exception as e:
        messages.error(request, f"Error adding location: {e}")
        form = LocationForm()
    return render(request, 'master/location_form.html', {'form': form, 'action': 'Add', 'username': username})


@login_required
def location_edit(request, pk):
    username = request.user.username
    try:
        loc = get_object_or_404(Location, location_id=pk)
        if request.method == 'POST':
            form = LocationForm(request.POST, instance=loc)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.updated_by = username
                obj.save()
                messages.success(request, "Location updated successfully.")
                return redirect('location_list')
        else:
            form = LocationForm(instance=loc)
    except Exception as e:
        messages.error(request, f"Error updating location: {e}")
        form = LocationForm()
    return render(request, 'master/location_form.html', {'form': form, 'action': 'Edit', 'username': username})


@login_required
def location_detail(request, pk):
    username = request.user.username
    try:
        loc = get_object_or_404(Location, location_id=pk)
    except Exception as e:
        messages.error(request, f"Error loading location details: {e}")
        return redirect('location_list')
    return render(request, 'master/location_detail.html', {'loc': loc, 'username': username})


@login_required
def location_delete(request, pk):
    username = request.user.username
    try:
        loc = get_object_or_404(Location, location_id=pk)
        if dbq.is_location_used(pk):
            messages.warning(request, "Cannot delete — location is used by other records.")
            return redirect('location_list')

        if request.method == 'POST':
            loc.delete()
            messages.success(request, "Location deleted successfully.")
            return redirect('location_list')
    except Exception as e:
        messages.error(request, f"Error deleting location: {e}")
        return redirect('location_list')

    return render(request, 'master/location_detail.html', {'loc': loc, 'confirm_delete': True, 'username': username})
