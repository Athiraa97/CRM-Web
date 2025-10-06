from django.db import models
import uuid
from datetime import datetime
from Master.models import *
# Create your models here.

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empno = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    join_date = models.DateField(null=True, blank=True)
    emp_start_date = models.DateField(null=True, blank=True)
    emp_end_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=(('active','Active'), ('inactive','Inactive')),
    default='active')
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    created_by = models.CharField(max_length=150,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    updated_by = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return f"{self.empno} - {self.name}"

class Skills(models.Model):
    employee = models.ForeignKey(Employee, related_name='skills', on_delete=models.CASCADE)
    skills_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    created_by = models.CharField(max_length=150,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    updated_by = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return self.name
