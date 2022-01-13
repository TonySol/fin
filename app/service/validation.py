"""Module with a class used to validate user input before calling services"""

from datetime import date, datetime

from app import db
from app.models.model import Department


class Validation:
    """Holds custom private methods to validate user input

    In the future can be replaced with ready-made WTForms validation
    – `validate` class method aggregates all methods and can be called from outside of the class
    """
    TABLE_NAME = None

    @staticmethod
    def __check_col_exist(table_name, col_name):
        columns = [column.key for column in table_name.__table__.columns]
        if col_name not in columns:
            return False
        return True

    @staticmethod
    def __get_col_datatype(table_name, col_name):
        return getattr(table_name, col_name).type.python_type

    @staticmethod
    def __get_col_length(table_name, col_name):
        try:
            return getattr(table_name, col_name).type.length
        except AttributeError:
            return False

    @staticmethod
    def __check_integer(value):
        try:
            value = int(value)
            if 0 > value < 2147483647:
                return f"The {value} exceeds the max length."
            return True
        except ValueError:
            return f"\"{value}\" is not of required data type."

    @staticmethod
    def __check_string(value):
        if any(not c.isalpha() for c in value):
            if any(c.isspace() for c in value):
                return True
            else:
                return f"The {value} should contain letters only."
        return True

    @staticmethod
    def __check_date_string(value):
        try:
            date_input = date.fromisoformat(value)
            if date(1940, 1, 1) > date_input < date(2006, 1, 1):
                return f"Have some sympathy, the man is out of appropriate age to exploit him"
            return True
        except ValueError:
            return f"The {value} should be of \"Year-Mon-Date\" or ISO format."

    @staticmethod
    def __check_dept_exist(name):
        if db.session.query(Department).filter_by(name=name).all():
            return True
        return "Failed: check if such department exists."

    @classmethod
    def validate(cls, form_data):
        """Aggregates all methods to call from outside of the class and validate user input

        Checks if required entry exists in the parent table.
        Obtains DB column requirements from the model (datatype, max length, etc).
        Checks user input against DB requirements.
        :param cls: provides class of the service thus class of model to check against
        :type cls: :class:
        :param form_data: unvalidated user input in the form of dict.
        :type form_data: dict
        :return: dict with user input or string with description of validation fail.
        """
        if cls.__name__ == "EmployeeService" and form_data["dept_name"] \
                and cls.__check_dept_exist(form_data["dept_name"]) is not True:
            return "Failed: check if such department exists."
        elif cls.__name__ == "DepartmentService" and form_data["name"] \
                and cls.__check_dept_exist(form_data["name"]) is True:
            return "Failed: The department with such name already exists."

        else:
            for key, value in form_data.items():
                if cls.__check_col_exist(cls.TABLE_NAME, key) is not True:
                    return f"The table does not contain [{key}] column name."

                data_type = cls.__get_col_datatype(cls.TABLE_NAME, key)
                max_length = cls.__get_col_length(cls.TABLE_NAME, key)

                if value:
                    if isinstance(value, str) and value.isspace():
                        return f"Empty [{key}] field is not allowed"

                    elif max_length and (len(value) > max_length or len(value) > 2000000):
                        return f"The {value} should be positive and fit max length of [{key}]."

                    elif isinstance(int(1), data_type) and cls.__check_integer(value) is not True:
                        return cls.__check_integer(value)

                    elif isinstance(str("a"), data_type) and cls.__check_string(value) is not True:
                        return cls.__check_string(value)

                    elif not isinstance(value, datetime) and isinstance(date.today(), data_type) \
                            and cls.__check_date_string(value) is not True:
                        return cls.__check_date_string(value)

        return form_data
