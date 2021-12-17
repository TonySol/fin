"""DB Modelstored here

Works via flask-sqlalchemy
"""
from init import db

class Department(db.Model):
    """Parent table for Employee"""
    name = db.Column(db.String(20), primary_key=True, index=True, unique=True)
    employees = db.relationship('Employee', backref='department', passive_deletes=True,  lazy=True)

    def __repr__(self):
        return self.name


class Employee(db.Model):
    """Table for employees data

    :dept_name: is a foreign key for a Department table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    date_of_bidth = db.Column(db.Date, index=True)
    salary = db.Column(db.Integer, nullable=False)
    dept_name = db.Column(db.String(20), db.ForeignKey('department.name', ondelete='CASCADE'))

    def __repr__(self):
        return f"This is employee. – {self.name}, {self.surname} from dept – {self.dept_name}."
