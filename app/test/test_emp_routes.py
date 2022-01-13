from datetime import date
from unittest import main

from app.test import TestBase

from app import db
from app.models.model import Department, Employee


class TestWebViews(TestBase):
    DEPT_FORM_ADD = {"name": "Add"}
    DEPT_FORM_EDIT = {"id": 2, "name": "Edit"}
    EMP_FORM = {"id": 4, "name": "Vova", "surname": "Thi Lvova",
                "date_of_bidth": None, "salary": 1500, "dept_name": "TestDept"}

    @classmethod
    def setUp(cls):
        """Makes a test db in temp file, populates it and pushes app context

        creates a test client, which allows to preserve a request context after request was handled
        this helps get all request execution details for tests,
        """
        super().setUp()

        dept1 = Department(name="TestDept")
        dept2 = Department(name="DeptDelete")
        emp1 = Employee(id=1, name="John", surname="Smith", date_of_bidth=date(2000, 1, 1),
                        salary=1503,
                        dept_name="TestDept")
        emp2 = Employee(id=2, name="Delete", surname="Me", date_of_bidth=date(2000, 1, 1),
                        salary=1000, dept_name="DeptOne")
        db.session.add(dept1)
        db.session.add(dept2)
        db.session.add(emp1)
        db.session.add(emp2)

        db.session.commit()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

        response = self.client.get('/index')
        self.assertEqual(200, response.status_code)

    def test_404(self):
        response = self.client.get('/not_exist')
        self.assertEqual(404, response.status_code)

    def test_employees(self):
        response = self.client.get('/employees')
        self.assertEqual(200, response.status_code)

    def test_search(self):
        response = self.client.post('/employees/search',
                                    data={"start_date": "", "end_date": date(2001, 1, 1)})
        self.assertEqual(200, response.status_code)
        self.assertTrue(b'John' in response.data)

        # negative
        response = self.client.post('/employees/search',
                                    data={"start_date": date(2001, 1, 1), "end_date": ""})
        self.assertEqual(200, response.status_code)
        self.assertFalse(b'John' in response.data)

    def test_add_employee(self):
        response = self.client.post('/employees/add', data=self.EMP_FORM, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_edit_employee(self):
        response = self.client.post('/employees/edit', data=self.EMP_FORM, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_delete_employee(self):
        response = self.client.post('/employees/delete', data={"id": 2}, follow_redirects=True)
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    main()
