from datetime import date

class Validation:
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
            if 0 < value < 2147483647:
                return f"The {value} exceeds the max length."
            return True
        except ValueError:
            return f"The {value} is not of required data type."

    @staticmethod
    def __check_string(value):
        if any(not c.isalpha() for c in value):
            if any(c.isspace() for c in value):
                return True
            else:
                return f"The {value} should contain letters only."
        return True

    @staticmethod
    def __check_date(value):
        try:
            date_input = date.fromisoformat(value)
            if date(1940, 1, 1) < date_input < date(2006, 1, 1):
                return f"Have some sympathy, the man is out of appropriate age to exploit him"
            return True
        except ValueError:
            return f"The {value} should be of \"Year-Mon-Date\" or ISO format."

    @classmethod
    def validate(cls, form_data):
        for key, value in form_data.items():
            data_type = cls.__get_col_datatype(cls.TABLE_NAME, key)
            max_length = cls.__get_col_length(cls.TABLE_NAME, key)

            if value:
                if cls.__check_col_exist(cls.TABLE_NAME, key) is not True:
                    return f"The table does not contain [{key}] column name."

                elif value.isspace():
                    return f"Empty [{key}] field is not allowed"

                elif max_length and (len(value) > max_length or len(value) > 2000000):
                    return f"The {value} should be positive and comply with max length of [{key}]."

                elif isinstance(int(1), data_type):
                    if cls.__check_integer(value) is not True:
                        return cls.__check_integer(value)

                elif isinstance(str("a"), data_type):
                    if cls.__check_string(value) is not True:
                        return cls.__check_string(value)

                elif isinstance(date.today(), data_type):
                    if cls.__check_date(value) is not True:
                        return cls.__check_date(value)

        return form_data
