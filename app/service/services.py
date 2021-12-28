from sqlalchemy import func

from app import db
from app.models import Department, Employee


class Service:
    TABLE_NAME = None

    def paginate(self):
        """self contains the function
            cls is just a name to pass a class value
            kwargs pass with func call in views
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
    def get_by_prime_key(cls, key):
        return db.session.query(cls.TABLE_NAME).get(key)

    @classmethod
    def add_entry(cls, **kwargs):
        db.session.add(cls.TABLE_NAME(**kwargs))
        db.session.commit()

    @classmethod
    def edit_entry(cls, dict_of_edits):
        employee = db.session.query(cls.TABLE_NAME).get(dict_of_edits["id"])
        for key, value in dict_of_edits.items():
            if value:
                setattr(employee, key, value)
        db.session.commit()

    @classmethod
    def delete_by_prime_key(cls, id):
        result = db.session.query(cls.TABLE_NAME).filter_by(id=id).delete()
        db.session.commit()
        return result

    @classmethod
    @paginate
    def get_all_by_filters(cls, **kwargs):
        return db.session.query(cls.TABLE_NAME).filter_by(**kwargs)


class DepartmentService(Service):
    TABLE_NAME = Department

    @classmethod
    @Service.paginate
    def get_avg_salary(cls):
        return db.session.query(Department.name, func.avg(Employee.salary)) \
            .select_from(Department).join(Employee) \
            .group_by(Department.name)


    @classmethod
    def delete_by_prime_key(cls, id):
        result = db.session.query(cls.TABLE_NAME).filter_by(name=id).delete()
        db.session.commit()
        return result

class EmployeeService(Service):
    TABLE_NAME = Employee

    @Service.paginate
    def hello():
        return db.session.query(Employee)

    @classmethod
    @Service.paginate
    def search_by_date(cls, **kwargs):
        return db.session.query(Employee) \
            .filter(Employee.date_of_bidth >= kwargs["start_date"]) \
            .filter(Employee.date_of_bidth <= kwargs["end_date"]) \
            .order_by(Employee.dept_name)
