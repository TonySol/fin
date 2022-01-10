import os
import tempfile
from datetime import date
from unittest import TestCase, main

from config import Test
from app import start_app, db
from app.models.model import Department, Employee
from app.service.services import DepartmentService, EmployeeService


class TestServices(TestCase):
    @classmethod
    def setUpClass(cls):
        """Create an instance of an app, get access to specific app context,
        push – bind the request context to the current app context.

        Makes a test db in temp file and populates it"""
        cls.file_handle, cls.file_path = tempfile.mkstemp()
        Test.SQLALCHEMY_DATABASE_URI = f'sqlite:///{cls.file_path}'

        cls.app = start_app(Test)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()

        dept1 = Department(name="Test_dept1")
        dept2 = Department(name="Test_dept2")
        emp1 = Employee(id=1, name="John", surname="Smith", date_of_bidth=date(2000, 1, 1),
                        salary=1503,
                        dept_name="Test_dept1")
        emp2 = Employee(id=2, name="Ostin", surname="Powers", date_of_bidth=date(1990, 1, 1),
                        salary=1500,
                        dept_name="Test_dept1")
        emp3 = Employee(id=3, name="Black", surname="Widow", date_of_bidth=date(1960, 1, 1),
                        salary=999,
                        dept_name="Test_dept2")
        db.session.add(dept1)
        db.session.add(dept2)
        db.session.add(emp1)
        db.session.add(emp2)
        db.session.add(emp3)

        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Removes db session, removes db file by closing link to the temp file.
        Removes request and app context by calling teardown functions."""
        db.session.remove()
        os.close(cls.file_handle)
        os.unlink(cls.file_path)
        cls.app_context.pop()

    def test_get_all(self):
        result = DepartmentService.get_all()
        self.assertEqual(db.session.query(Department).all(), result)

        result_paginated = DepartmentService.get_all(paginate=True)
        self.assertEqual("Pagination", result_paginated.__class__.__name__)

    def test_get_by_id(self):
        self.assertIsNotNone(DepartmentService.get_by_id(1))
        self.assertIsNone(DepartmentService.get_by_id(5))

    def test_add_entry(self):
        entry = {"id": 4, "name": "Vova", "surname": "ThiLvova",
                 "date_of_bidth": date(1980, 1, 1), "salary": 1500, "dept_name": "Test_dept2"}

        EmployeeService.add_entry(entry)
        self.assertIsNotNone(db.session.query(Employee).get(4))

        DepartmentService.add_entry({"name":"New"})
        self.assertTrue(db.session.query(Department).filter_by(name="New"))

    def test_edit_entry(self):
        EmployeeService.edit_entry({"id": 1, "surname": "Wick"})
        result = db.session.query(Employee).get(1).surname
        self.assertEqual("Wick", result)

    def test_delete_by_id(self):
        before_result = db.session.query(Department).count()
        DepartmentService.delete_by_id(2)
        result = db.session.query(Department).count()
        self.assertEqual(before_result - 1, result)

    def test_get_all_by_filters(self):
        result = EmployeeService.get_all_by_filters(dept_name="Test_dept1", salary=1503)
        self.assertEqual(1, len(result))
        self.assertEqual("John", result[0].name)

        result_paginated = EmployeeService.get_all_by_filters(paginate=True,
                                                              dept_name="Test_dept1", salary=1503)
        self.assertEqual("Pagination", result_paginated.__class__.__name__)

    def test_get_avg_salary(self):
        result = DepartmentService.get_avg_salary()
        self.assertEqual(1502, result[0][2])

        result_paginated = DepartmentService.get_avg_salary(paginate=True)
        self.assertEqual("Pagination", result_paginated.__class__.__name__)

    def test_search_by_date(self):
        result = EmployeeService.search_by_date(start_date=date(2000, 1, 1),
                                                end_date=date(2020, 1, 1))
        self.assertEqual("John", result[0].name)

        result2 = EmployeeService.search_by_date(start_date=date(1990, 1, 1),
                                                 end_date=date(2020, 1, 1))
        self.assertEqual(2, len(result2))

        result_paginated = EmployeeService.search_by_date(paginate=True,
                                                          start_date=date(1960, 1, 1),
                                                          end_date=date(2020, 1, 1))
        self.assertEqual("Pagination", result_paginated.__class__.__name__)

        # negative test
        result_negative = EmployeeService.search_by_date(start_date=date(2020, 1, 1),
                                                         end_date=date(2019, 1, 1))
        self.assertFalse(result_negative)


if __name__ == "__main__":
    main()
