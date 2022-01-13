from datetime import date
from unittest import main

from app.test import TestBase

from app import db
from app.models.model import Department
from app.service.services import EmployeeService, DepartmentService


class TestValidation(TestBase):
    CORRECT = {"name": "Vova", "surname": "Thi Lvova", "salary": 1000,
                "date_of_bidth": date(1980, 1, 1).isoformat(), "dept_name": "TestDept"}

    DEPARTMENT = {"name": "TestDept"}

    WRONG_KEY = {"no name": "Vova", "dept_name": "TestDept"}
    SPACED_VALUE ={"name": " ", "dept_name": "TestDept"}
    MAX_LENGTH = {"surname": "Thi Lvova Twentry One", "dept_name": "TestDept"}
    WRONG_INT = {"salary": "mor", "dept_name": "TestDept"}
    WRONG_STR = {"name": "1Vova/", "dept_name": "TestDept"}
    WRONG_DATE ={"date_of_bidth": "11", "dept_name": "TestDept"}

    def setUp(cls):
        super().setUp()

        dept1 = Department(name="TestDept")
        db.session.add(dept1)
        db.session.commit()

    def test_validate(self):
        result = EmployeeService.validate(self.CORRECT)
        self.assertIsInstance(result, dict)

        result = EmployeeService.validate(self.WRONG_KEY)
        self.assertIsInstance(result, str)

        result = EmployeeService.validate(self.SPACED_VALUE)
        self.assertIsInstance(result, str)

        result = EmployeeService.validate(self.MAX_LENGTH)
        self.assertIsInstance(result, str)

        result = EmployeeService.validate(self.WRONG_INT)
        self.assertIsInstance(result, str)

        result = EmployeeService.validate(self.WRONG_STR)
        self.assertIsInstance(result, str)

        result = EmployeeService.validate(self.WRONG_DATE)
        self.assertIsInstance(result, str)

        result = DepartmentService.validate(self.DEPARTMENT)
        self.assertIsInstance(result, str)

if __name__ == "__main__":
    main.run()