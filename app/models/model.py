"""Holds classes that define such database tables:

– `Department`: class for department model
– `Employee`: class for employee model
"""
# pylint: disable=too-few-public-methods
from app import db

class Department(db.Model):
    """This model defines department table

    – id: int primary key for department entries
    – name: str a name of the department entry


    –employees: a relationship to the child table. passive_deletes=True, for cascading mode.
    Parent for Employee table"""
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), unique=True)
    employees = db.relationship('Employee', backref='department', passive_deletes=True, lazy=True)

    def __repr__(self):
        """Returns string representation of department object
        :return: string representation of department object"""
        return f"{self.id}, {self.name}"


class Employee(db.Model):
    """This model defines employee table

    – id: int primary key for employee entries
    – name: str the employee's name
    – surname: str the employee's surname
    – date_of_bidth: date object the employee's birthday
    – salary:  int primary key for employee entries

    – dept_name: describes the relationship with the parent. set cascading on delete and update.
    Child of Departments table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    date_of_bidth = db.Column(db.Date, index=True)
    salary = db.Column(db.Integer, nullable=False)
    dept_name = db.Column(db.String(20), db.ForeignKey('department.name',
                                                       ondelete='CASCADE', onupdate='CASCADE'))

    def __repr__(self):
        """Returns string representation of employee object
        :return: string representation of employee object"""
        return f"This is employee. – {self.name}, {self.surname} from dept – {self.dept_name}."
