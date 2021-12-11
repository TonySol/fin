import sys

sys.path.append("..")
from init import db


class Department(db.Model):
    name = db.Column(db.String(20), primary_key=True, index=True, unique=True)
    employees = db.relationship('Employee', backref='department', lazy=True)

    def __repr__(self):
        return self.name


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    date_of_bidth = db.Column(db.Date, index=True)
    salary = db.Column(db.Integer, nullable=False)
    dept_name = db.Column(db.String(20), db.ForeignKey('department.name'), nullable=False)

    def __repr__(self):
        return f"This is employee. – {self.name}, {self.surname} from dept – {self.dept_name}."
