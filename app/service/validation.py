"""Module with a class used to validate user input before calling services"""

from datetime import date, datetime

from app import db
from app.models.model import Department


class Validation:
    # pylint: disable=too-many-return-statements, too-few-public-methods
    """Holds custom private methods to validate user input

    In the future can be replaced with ready-made WTForms validation
    – `validate` class method aggregates all methods and can be called from outside of the class
    """
    TABLE_NAME = None

    @staticmethod
    def __check_col_exist(table_name, col_name):
        columns = [column.key for column in table_name.__table__.columns]
        return bool(col_name in columns)

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
        if isinstance(value, int) or value.isdigit():
            return True if 0 < int(value) < 2147483647 \
                        else f"The {value} exceeds the max length."
        return f"\"{value}\" is not of required data type."


    @staticmethod
    def __check_date(value):
        date_input = value
        if not isinstance(value, datetime):
            try:
                date_input = datetime.fromisoformat(value)
            except ValueError:
                return f"The {value} should be of \"Year-Mon-Date\" or ISO format."

        return True if datetime(1940, 1, 1) < date_input < datetime(2006, 1, 1) \
            else "Have some sympathy, the man is out of appropriate age to exploit him"

    @staticmethod
    def __check_dept_exist(name):
        return True if db.session.query(Department).filter_by(name=name).all() \
                    else "Failed: check if such department exists."

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
        if cls.__name__ == "DepartmentService" and form_data["name"] \
                and cls.__check_dept_exist(form_data["name"]) is True:
            return "Failed: The department with such name already exists."

        for key, value in form_data.items():
            if cls.__check_col_exist(cls.TABLE_NAME, key) is not True:
                return f"The table does not contain [{key}] column name."

            data_type = cls.__get_col_datatype(cls.TABLE_NAME, key)
            max_length = cls.__get_col_length(cls.TABLE_NAME, key)

            if value:
                if isinstance(value, str) and value.isspace():
                    return f"Empty [{key}] field is not allowed."

                if max_length and (len(value) > max_length or len(value) > 2000000):
                    return f"The {value} should be positive and fit max length of [{key}]."

                if data_type is int and cls.__check_integer(value) is not True:
                    return cls.__check_integer(value)

                if data_type is str and not value.replace(" ", "").isalpha():
                    return f"The {value} should contain letters only."

                if data_type is date and cls.__check_date(value) is not True:
                    return cls.__check_date(value)

        return form_data
