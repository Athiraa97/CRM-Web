from django.db import connection


def fetch_employee_details():
    """
    Returns a list of employee details with joined department, location, designation, and skills.
    """
    sql = """
        SELECT e.id, e.empno, e.name, e.phone, e.status,
               d.dept_name AS department,
               l.loc_name AS location,
               des.des_name AS designation,
               GROUP_CONCAT(s.skills_name SEPARATOR ', ') AS skills
        FROM employees_employee e
        LEFT JOIN Master_department d ON e.department_id = d.department_id
        LEFT JOIN Master_location l ON e.location_id = l.location_id
        LEFT JOIN Master_designation des ON e.designation_id = des.designation_id
        LEFT JOIN employees_skills s ON e.id = s.employee_id
        GROUP BY e.id, e.empno, e.name, e.phone, e.status, d.dept_name, l.loc_name, des.des_name
        ORDER BY e.name;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result


def fetch_employees(filters=None):
    """
    Return list of employee rows.
    filters is an optional dict (e.g., {'name': 'John', 'date_from': '2024-01-01'})
    """
    sql = """
        SELECT e.id, e.empno, e.name, e.phone, e.status,
               d.dept_name AS department,
               l.loc_name AS location,
               des.des_name AS designation,
               GROUP_CONCAT(s.skills_name SEPARATOR ', ') AS skills
        FROM employees_employee e
        LEFT JOIN Master_department d ON e.department_id = d.department_id
        LEFT JOIN Master_location l ON e.location_id = l.location_id
        LEFT JOIN Master_designation des ON e.designation_id = des.designation_id
        LEFT JOIN employees_skills s ON e.id = s.employee_id
        GROUP BY e.id, e.empno, e.name, e.phone, e.status, d.dept_name, l.loc_name, des.des_name
        ORDER BY e.name;
    """
    params = []

    if filters:
        if 'name' in filters and filters['name']:
            sql += " AND name LIKE %s"
            params.append(f"%{filters['name']}%")

        if 'date_from' in filters and filters['date_from']:
            sql += " AND join_date >= %s"
            params.append(filters['date_from'])

        if 'date_to' in filters and filters['date_to']:
            sql += " AND join_date <= %s"
            params.append(filters['date_to'])

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        cols = [c[0] for c in cursor.description]
        rows = [dict(zip(cols, row)) for row in cursor.fetchall()]

    return rows

