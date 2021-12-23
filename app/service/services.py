from app import db
from app.models import Department, Employee

class DepartmetnService:
    def get_department():
        return db.session.query(Department).all()