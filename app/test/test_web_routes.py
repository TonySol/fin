import os
import tempfile
from datetime import date

from unittest import TestCase, main

from config import Test
from app import start_app, db
from app.models.model import Department, Employee

class TestWebViews(TestCase):
    @classmethod
    def setUpClass(cls):
        """Makes a test db in temp file, populates it and pushes app context

        creates a test client, which allows to preserve a request context after request was handled
        this helps get all request execution details for tests,
        """
        cls.file_handle, cls.file_path = tempfile.mkstemp()
        Test.SQLALCHEMY_DATABASE_URI = f'sqlite:///{cls.file_path}'

        cls.app = start_app(Test)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()
        dept1 = Department(name="Test_dept1")
        emp1 = Employee(id=1, name="John", surname="Smith", date_of_bidth=date(2000, 1, 1),
                        salary=1503,
                        dept_name="Test_dept1")
        db.session.add(dept1)
        db.session.add(emp1)

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Removes db by closing link to the temp file, and removes app context

        Call destruction of request and app context manually, because test_client blocks the
        automatic stack clean up. Or unittest will leak memory."""
        db.session.remove()
        os.close(cls.file_handle)
        os.unlink(cls.file_path)

        cls.app_context.pop()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

        response = self.client.get('/index')
        self.assertEqual(200, response.status_code)

    def test_404(self):
        response = self.client.get('/not_exist')
        self.assertEqual(404, response.status_code)

    def test_departments(self):
        response = self.client.get('/departments')
        self.assertEqual(200, response.status_code)

    def test_department(self):
        response = self.client.get('/department/Test_dept1/')
        self.assertEqual(200, response.status_code)


    def test_employees(self):
        response = self.client.get('/employees')
        self.assertEqual(200, response.status_code)

    def test_employees_add(self):
        data = {"id": 4, "name": "Vova", "surname": "ThiLvova",
                 "date_of_bidth": date(1980, 1, 1), "salary": 1500, "dept_name": "Test_dept1"}
        response = self.client.post('/employees/add', data=data, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_employees_edit(self):
        data = {"id": 1, "name": "Vova"}
        response = self.client.post('/employees/edit', data=data, follow_redirects=True)
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    main()