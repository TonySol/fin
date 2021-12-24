from sqlalchemy import func

from app import db
from app.models import Department, Employee


class DepartmentService:

    @classmethod
    def get_all(cls, paginate=False, per_page=2, page=1, error_out=True):
        if paginate:
            return db.session.query(Department)\
                    .paginate(per_page=per_page, page=page, error_out=error_out)
        return db.session.query(Department).all()

    @classmethod
    def get_by_name(cls, name):
        return db.session.query(Department).get(name)

    @classmethod
    def add_entry(cls, name):
        db.session.add(Department(name=name))
        db.session.commit()

    @classmethod
    def get_avg_salary(cls, paginate=False, per_page=2, page=1, error_out=True, **kwargs):
        if paginate:
            return db.session.query(Department.name, func.avg(Employee.salary)) \
                                .select_from(Department).join(Employee) \
                                .group_by(Department.name)\
                                .paginate(per_page=per_page, page=page, error_out=error_out)
        return db.session.query(Department.name, func.avg(Employee.salary)) \
                                .select_from(Department).join(Employee) \
                                .group_by(Department.name).all()


class EmployeeService:
    @classmethod
    def get_all(cls, paginate=False, per_page=2, page=1, error_out=True):
        if paginate:
            return db.session.query(Employee)\
                    .paginate(per_page=per_page, page=page, error_out=error_out)
        return db.session.query(Employee).all()

    @classmethod
    def get_by_id(cls, id):
        return db.session.query(Employee).get(id)

    @classmethod
    def add_entry(cls, **kwargs):
        db.session.add(Employee(**kwargs))
        db.session.commit()

    @classmethod
    def edit_entry(cls, dict_of_edits):
        employee = db.session.query(Employee).get(dict_of_edits["id"])
        for key, value in dict_of_edits.items():
            if value:
                setattr(employee, key, value)
        db.session.commit()

    @classmethod
    def delete_by_id(cls, id):
        result = db.session.query(Employee).filter_by(id=id).delete()
        db.session.commit()
        return result

    @classmethod
    def search_by_date(cls, **kwargs):
        pass

    @classmethod
    def get_all_by_filters(cls, paginate=False, per_page=2, page=1, error_out=True, **kwargs):
        if paginate:
            return db.session.query(Employee)\
                    .filter_by(**kwargs)\
                    .paginate(per_page=per_page, page=page, error_out=error_out)
        return db.session.query(Employee).filter_by(**kwargs).all()