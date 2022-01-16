"""Module holds services to fetch the database.

– `Service` class contains base methods for db fetching
– `DepartmentService` class holds department specific methods
– `EmployeeService` class holds department specific methods
"""
from sqlalchemy import func, desc

from app import db
from app.models.model import Department, Employee
from app.service.validation import Validation



class Service:
    """Contains base methods for db fetching:

    – `paginate` decorates db queries with pagination or all methods
    – `get_all` returns database BaseQuery for a table
    – `get_by_id` returns database query for specific entry by its id
    – `add_entry` creates new entry in db
    – `edit_entry` edits db entry based on input data
    – `delete_by_id` deletes db entry by id
    – `get_all_by_filters` returns database query with filters

    – TABLE_NAME: base parameter to pass model name from where the method call was made.
    – TABLE_NAME type: :class: name of the db model class
    """
    TABLE_NAME = None

    def paginate(self):
        """Decorates db queries with paginate\all methods.

        – self: holds a decorated method with BaseQuery
        – cls: is just a name to pass arguments of a decorated function

        wrapper kwargs used to preserve arguments provided with original method call
        :return: database query call with paginate\all method
        """

        def wrapper(cls, paginate=False, per_page=10, page=1, **kwargs):
            # pylint: disable=not-callable
            if paginate:
                return self(cls, **kwargs).paginate(per_page=per_page, page=page)
            return self(cls, **kwargs).all()

        return wrapper

    @staticmethod
    def __remove_id_val(form_data):
        return {k: v for k, v in form_data.items() if k != "id"}

    @classmethod
    @paginate
    def get_all(cls):
        """Returns database BaseQuery for a table"""
        return db.session.query(cls.TABLE_NAME)

    @classmethod
    def get_by_id(cls, value):
        """Returns database query for specific entry by its id

        :param value: id of the desired entry
        :type value: int, but can be any based on model that is being fetched
        :return: database BaseQuery call with specified entry id
        """
        return db.session.query(cls.TABLE_NAME).get(value)

    @classmethod
    def add_entry(cls, form_data):
        """Creates new entry in the db

        Calls private method to remove id item from the dict provided by the user, if such exists.
        Adds entry to the database.

        :param form_data: dict with value for the new entry in form column_name:value
        :type form_data: dict
        """
        # pylint: disable=not-callable
        id_removed = cls.__remove_id_val(form_data)
        db.session.add(cls.TABLE_NAME(**id_removed))
        db.session.commit()

    @classmethod
    def edit_entry(cls, form_data):
        """Edits existing entry in the db

        Checks whether such entry exists.
        Calls private method to remove id item from the dict provided by the user, if such exists.
        Edits entry to the database.

        :param form_data: dict with values for editing in form column_name:value
        :type form_data: dict
        :return: True on success, False if no entry to edit.
        """
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
    def delete_by_id(cls, value):
        """Deletes db entry by id

        :param value: id of the desired entry
        :type value: int, but can be any based on model that is being edited
        :return: number of entries that was checnged by delete method
        """
        result = db.session.query(cls.TABLE_NAME).filter_by(id=value).delete()
        db.session.commit()
        return result

    @classmethod
    @paginate
    def get_all_by_filters(cls, **kwargs):
        """Returns database query with filters applied

        :param kwargs: accepts only on key/value pair to search for
        :type kwargs: dict

        :return: database BaseQuery with specified fields to look for
        """
        return db.session.query(cls.TABLE_NAME).filter_by(**kwargs)


class DepartmentService(Service, Validation):
    """Contains methods for Department table fetching:

    – `get_avg_salary` orders department table based on the employees average salary.

    – TABLE_NAME: name of the table to use in the db queries
    – TABLE_NAME type: :class: name of the db model class
    """
    TABLE_NAME = Department

    @classmethod
    @Service.paginate
    def get_avg_salary(cls):
        """Orders department table based on the employees average salary.

        Outer join to get all fields from both tables, thus including departments without employees.
        Group by include id and name, in order to provide department id into controller.
        Apply func round, func avg to get the average salary, and label it for convenience.
        """
        return db.session \
            .query(Department.id, Department.name,
                   func.round(func.avg(Employee.salary)).label("avg_salary")) \
            .select_from(Department).outerjoin(Employee) \
            .group_by(Department.id, Department.name).order_by(desc("avg_salary"))


class EmployeeService(Service, Validation):
    """Contains methods for Employee table fetching:

    – `search_by_date` returns query for filtering result by `date_of_bidth` values.

    – TABLE_NAME: name of the table to use in the db queries
    – TABLE_NAME type: :class: name of the db model class
    """
    TABLE_NAME = Employee

    @classmethod
    @Service.paginate
    def search_by_date(cls, **kwargs):
        """Returns BaseQuery to fetch db filtered by date provided in dict

        :param kwargs: a dict of two items "start_date" and "end_date"
        :type kwargs: dict
        :return: query to filter db based on provided `date_of_bidth` values
        """
        return db.session.query(Employee) \
            .filter(Employee.date_of_bidth >= kwargs["start_date"]) \
            .filter(Employee.date_of_bidth <= kwargs["end_date"]) \
            .order_by(Employee.dept_name)
