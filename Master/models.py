from django.db import models
import uuid
from datetime import datetime

# Create your models here.

class Department(models.Model):
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dept_name = models.CharField(max_length=255, unique=True)
    dept_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    created_by = models.CharField(max_length=150,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    updated_by = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return self.dept_name
    

class Designation(models.Model):
    designation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='designations')
    des_name = models.CharField(max_length=255)
    des_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    created_by = models.CharField(max_length=150,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    updated_by = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return f"{self.des_name} ({self.department.dept_name})"
    
class Location(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loc_name = models.CharField(max_length=255, unique=True)
    loc_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    created_by = models.CharField(max_length=150,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    updated_by = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return self.loc_name