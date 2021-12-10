import sys
sys.path.append("..")
from init import db

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    descr = db.Column(db.String(50))

    def __repr__(self):
        return f"Name of dept. – {self.name}, with id – {self.id}."