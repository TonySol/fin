from datetime import date
from sqlalchemy import func, desc

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

    @staticmethod
    def __remove_id_val(form_data):
        return {k: v for k, v in form_data.items() if k != "id"}

    @classmethod
    @paginate
    def get_all(cls):
        return db.session.query(cls.TABLE_NAME)

    @classmethod
    def get_by_id(cls, key):
        return db.session.query(cls.TABLE_NAME).get(key)

    @classmethod
    def add_entry(cls, form_data):
        id_removed = cls.__remove_id_val(form_data)
        db.session.add(cls.TABLE_NAME(**id_removed))
        db.session.commit()

    @classmethod
    def edit_entry(cls, form_data):
        entry = cls.get_by_id(form_data["id"])
        if entry:
            id_removed = cls.__remove_id_val(form_data)
            for key, value in id_removed.items():
                if value:
                    setattr(entry, key, value)
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
        return db.session\
                .query(Department.id, Department.name, func.round(func.avg(Employee.salary)).label("avg_salary")) \
                .select_from(Department).outerjoin(Employee) \
                .group_by(Department.id, Department.name).order_by(desc("avg_salary"))


class EmployeeService(Service, Validation):
    TABLE_NAME = Employee

    @classmethod
    @Service.paginate
    def search_by_date(cls, **kwargs):
        return db.session.query(Employee) \
                .filter(Employee.date_of_bidth >= kwargs["start_date"]) \
                .filter(Employee.date_of_bidth <= kwargs["end_date"]) \
                .order_by(Employee.dept_name)
