from sqlalchemy import func

from app import db
from app.models import Department, Employee


class DepartmentService:

    @classmethod
    def get_all(cls):
        return db.session.query(Department)

    @classmethod
    def get_by_name(cls, name):
        return db.session.query(Department).get(name)

    @classmethod
    def add_dept(cls, name):
        db.session.add(Department(name=name))
        db.session.commit()

    @classmethod
    def get_avg_salary(cls):
        return db.session.query(Department.name, func.avg(Employee.salary)) \
                                .select_from(Department).join(Employee) \
                                .group_by(Department.name)

class EmployeeService:

    def get_all(cls):
        return db.session.query(Employee)

    @classmethod
    def get_by_id(cls, id):
        return db.session.query(Employee).get(id)

    @classmethod
    def add_emp(cls, **kwargs):
        db.session.add(Employee(**kwargs))
        db.session.commit()

    @classmethod
    def edit_emp(cls, id, dict_of_edits):
        employee = db.session.query(Employee).get(id)
        for key, value in dict_of_edits.items():
            if value:
                setattr(employee, key, value)
        db.session.commit()