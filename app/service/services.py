from datetime import date
from sqlalchemy import func

from app import db
from .validation import Validation
from app.models import Department, Employee


class Service:
    TABLE_NAME = None

    def paginate(self):
        """self holds a decorated function
            cls is just a name to pass a parameters of class function
            kwargs are passed from function call in views
        """

        def wrapper(cls, paginate=False, per_page=10, page=1, **kwargs):
            if paginate:
                return self(cls, **kwargs).paginate(per_page=per_page, page=page)
            else:
                return self(cls, **kwargs).all()

        return wrapper

    @classmethod
    @paginate
    def get_all(cls):
        return db.session.query(cls.TABLE_NAME)

    @classmethod
    def get_by_id(cls, key):
        return db.session.query(cls.TABLE_NAME).get(key)

    @classmethod
    def add_entry(cls, entry):
        db.session.add(cls.TABLE_NAME(**entry))
        db.session.commit()

    @classmethod
    def edit_entry(cls, entry, entry_id=None):
        if entry_id is None:
            entry_id = entry["id"]

        employee = cls.get_by_id(entry_id)
        if employee:
            for key, value in entry.items():
                if value:
                    setattr(employee, key, value)
            db.session.commit()
            return True
        return False

    @classmethod
    def delete_by_id(cls, id):
        result = db.session.query(cls.TABLE_NAME).filter_by(id=id).delete()
        db.session.commit()
        return result

    @classmethod
    @paginate
    def get_all_by_filters(cls, **kwargs):
        return db.session.query(cls.TABLE_NAME).filter_by(**kwargs)


class DepartmentService(Service, Validation):
    TABLE_NAME = Department

    @classmethod
    @Service.paginate
    def get_avg_salary(cls):
        return db.session.query(Department.name, func.round(func.avg(Employee.salary))) \
            .select_from(Department).join(Employee) \
            .group_by(Department.name)

    @classmethod
    def delete_by_id(cls, id):
        result = db.session.query(cls.TABLE_NAME).filter_by(name=id).delete()
        db.session.commit()
        return result


class EmployeeService(Service, Validation):
    TABLE_NAME = Employee

    @staticmethod
    def __dept_exists(dept_name):
        find_department = DepartmentService.get_by_id(dept_name)
        if not find_department:
            DepartmentService.add_entry({"name": dept_name})
            return True
        return True

    @classmethod
    @Service.paginate
    def search_by_date(cls, **kwargs):
        return db.session.query(Employee) \
            .filter(Employee.date_of_bidth >= kwargs["start_date"]) \
            .filter(Employee.date_of_bidth <= kwargs["end_date"]) \
            .order_by(Employee.dept_name)

    @classmethod
    def add_entry(cls, entry):
        if cls.__dept_exists(entry["dept_name"]):
            super().add_entry(entry)

    @classmethod
    def edit_entry(cls, entry, entry_id=None):
        if entry_id is None:
            entry_id = entry["id"]

        employee = cls.get_by_id(entry_id)
        dept_name = entry["dept_name"]

        if employee and cls.__dept_exists(dept_name):
            for key, value in entry.items():
                if value:
                    setattr(employee, key, value)
            db.session.commit()
            return True
        return False
