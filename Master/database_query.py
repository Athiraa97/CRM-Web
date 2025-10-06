from typing import List, Dict
from django.db import connection

def dictfetchall(cursor):
    """Convert cursor results to a list of dicts."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_departments() -> List[Dict]:
    sql = """
        SELECT 
            department_id, 
            dept_name, 
            dept_description, 
            created_at, 
            created_by, 
            updated_at, 
            updated_by 
        FROM Master_department
        ORDER BY dept_name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)

def is_department_used(department_id) -> bool:
    """Skip check since no related table exists yet."""
    return False

def get_designations() -> List[Dict]:
    sql = """
        SELECT 
            d.designation_id,
            d.des_name AS designation_name,
            d.des_description AS designation_description,
            d.department_id,
            dept.dept_name AS department_name,
            d.created_at,
            d.created_by,
            d.updated_at,
            d.updated_by
        FROM master_designation d
        JOIN master_department dept 
          ON d.department_id = dept.department_id
        ORDER BY dept.dept_name, d.des_name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)

def is_designation_used(designation_id) -> bool:
    """Skip check since no related table exists yet."""
    return 

def get_locations() -> List[Dict]:
    sql = """
        SELECT 
            location_id, 
            loc_name, 
            loc_description, 
            created_at, 
            created_by, 
            updated_at, 
            updated_by 
        FROM Master_location
        ORDER BY loc_name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)

def is_location_used(location_id) -> bool:
    """Skip check since no related table exists yet."""
    return False

def get_designations_by_department(department_id: int) -> List[Dict]:
    """Fetch all designations under a specific department."""
    sql = """
        SELECT 
            designation_id, 
            des_name AS designation_name
        FROM master_designation
        WHERE department_id = %s
        ORDER BY des_name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [department_id])
        return dictfetchall(cursor)
