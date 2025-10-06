
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Employee, Skills
from .forms import EmployeeForm, SkillFormSet
from . import database_query
from Master import database_query as db
import csv

@login_required
def employee_list(request):
    username = request.user.username
    filters = {}
    if request.GET.get('date_from'):
        filters['date_from'] = request.GET.get('date_from')
    if request.GET.get('date_to'):
        filters['date_to'] = request.GET.get('date_to')
    rows = database_query.fetch_employees(filters)
    return render(request, 'employees/employee_list.html', {
        'employees': rows, 'username': username
    })


@login_required
def employee_add(request):
    username = request.user.username
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        formset = SkillFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            print("Form is valid")
            emp = form.save(commit=False)
            emp.created_by = username
            emp.updated_by = username
            emp.save()

            formset.instance = emp
            formset.save()
            messages.success(request, 'Employee created successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
        formset = SkillFormSet()

    departments = db.get_departments()
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'formset': formset,
        'departments': departments,
        'username': username,
        'action': 'Add'
    })


@login_required
def employee_edit(request, pk):
    username = request.user.username
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=emp)
        formset = SkillFormSet(request.POST, instance=emp)
        if form.is_valid() and formset.is_valid():
            emp = form.save(commit=False)
            emp.updated_by = username
            emp.save()
            formset.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=emp)
        formset = SkillFormSet(instance=emp)

    departments = db.get_departments()
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'formset': formset,
        'departments': departments,
        'username': username,
        'action': 'Edit'
    })


@login_required
def ajax_designations(request):
    dept_id = request.GET.get('department_id')
    data = db.get_designations_by_department(dept_id)
    print("data: ",data)
    return JsonResponse({'designations': data})


@login_required
def ajax_locations(request):
    dept_id = request.GET.get('dept_id')
    data = db.get_locations(dept_id)
    return JsonResponse({'locations': data})
@login_required
def employee_detail(request, pk):
    username = request.user.username
    emp = get_object_or_404(Employee, pk=pk)
    skills = emp.skills.all().order_by('skills_name')  # Fetch all skills linked to this employee
    return render(request, 'employees/employee_detail.html', {
        'emp': emp,
        'skills': skills,
        'username': username
    })

@login_required
def employee_delete(request, pk):
    username = request.user.username
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp.delete()
        messages.success(request, 'Employee deleted')
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'object': emp,'username': username})



@login_required
def download_selected(request):
    username = request.user.username
    """POST with selected ids (comma separated)"""
    ids = request.POST.get('ids', '')
    if not ids:
        return HttpResponse('No ids', status=400)

    id_list = ids.split(',')
    employees = Employee.objects.filter(id__in=id_list)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees_selected.csv"'

    writer = csv.writer(response)
    # Write header
    writer.writerow([
        'Employee No', 'Name', 'Phone', 'Address', 'Join Date',
        'Employee Start Date', 'Employee End Date', 'Photo URL',
        'Status', 'Department', 'Designation', 'Location',
        'Created By', 'Created At', 'Updated By', 'Updated At'
    ])

    # Write data rows
    for e in employees:
        writer.writerow([
            e.empno,
            e.name,
            e.phone or '',
            e.address or '',
            e.join_date.strftime('%Y-%m-%d') if e.join_date else '',
            e.emp_start_date.strftime('%Y-%m-%d') if e.emp_start_date else '',
            e.emp_end_date.strftime('%Y-%m-%d') if e.emp_end_date else '',
            e.photo.url if e.photo else '',
            e.status,
            e.department if e.department else '',
            e.designation if e.designation else '',
            e.location if e.location else '',
            e.created_by or '',
            e.created_at.strftime('%Y-%m-%d %H:%M:%S') if e.created_at else '',
            e.updated_by or '',
            e.updated_at.strftime('%Y-%m-%d %H:%M:%S') if e.updated_at else ''
        ])

    return response

