from datetime import date
from unittest import main

from app.test import TestBase

from app import db
from app.models.model import Department, Employee


class TestWebViews(TestBase):
    DEPT_FORM_ADD = {"name": "Add"}
    DEPT_FORM_EDIT = {"id": 2, "name": "Edit"}
    DEPT_FORM_EDIT_WRONG = {"id": 5, "name": "EditWrong"}
    DEPT_FORM_WRONG_VALIDATION = {"id": 1, "name": ":sdfs/"}

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

        db.session.add(dept1)
        db.session.add(dept2)
        db.session.add(emp1)

        db.session.commit()

    def test_departments(self):
        response = self.client.get('/departments')
        self.assertEqual(200, response.status_code)

    def test_department(self):
        response = self.client.get('/department/TestDept/')
        self.assertEqual(200, response.status_code)

    def test_add_department(self):
        response = self.client.post('/department/add', data=self.DEPT_FORM_ADD,
                                    follow_redirects=True)
        self.assertEqual(200, response.status_code)

        # negative tests
        response = self.client.post('/department/add', data=self.DEPT_FORM_WRONG_VALIDATION,
                                    follow_redirects=True)
        self.assertTrue(b"add this entry" in response.data)

    def test_edit_department(self):
        response = self.client.post('/department/edit', data=self.DEPT_FORM_EDIT,
                                    follow_redirects=True)
        self.assertEqual(200, response.status_code)

        # negative tests
        response = self.client.post('/department/edit', data=self.DEPT_FORM_EDIT_WRONG,
                                    follow_redirects=True)
        self.assertTrue(b"id does not exists" in response.data)

        response = self.client.post('/department/edit', data=self.DEPT_FORM_WRONG_VALIDATION,
                                    follow_redirects=True)
        self.assertTrue(b"Could not edit the entry" in response.data)

    def test_delete_department(self):
        response = self.client.post('/department/delete', data={"id": 2},
                                    follow_redirects=True)
        self.assertEqual(200, response.status_code)

        # negative tests
        response = self.client.post('/department/delete', data=self.DEPT_FORM_EDIT_WRONG,
                                    follow_redirects=True)
        self.assertTrue(b"Could not delete the entry" in response.data)


if __name__ == "__main__":
    main()
