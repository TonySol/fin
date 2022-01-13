from datetime import date
from unittest import main

from app.test import TestBase

from app import db
from app.models.model import Department, Employee


class TestAPI(TestBase):
    DEPT_JSON = {"name": "Added"}
    EMP_JSON = {"name": "Vova", "surname": "Thi Lvova", "salary": 1000,
                "date_of_bidth": date(1980, 1, 1).isoformat(), "dept_name": "DeptOne"}

    @classmethod
    def setUp(cls):
        """Populates DB with required data"""
        super().setUp()
        dept1 = Department(name="DeptOne")
        dept2 = Department(name="DeptDelete")
        emp1 = Employee(id=1, name="John", surname="Smith", date_of_bidth=date(2000, 1, 1),
                        salary=1503, dept_name="DeptOne")
        emp2 = Employee(id=2, name="Delete", surname="Me", date_of_bidth=date(2000, 1, 1),
                        salary=1000, dept_name="DeptOne")

        db.session.add(dept1)
        db.session.add(dept2)
        db.session.add(emp1)
        db.session.add(emp2)

        db.session.commit()

    def test_get_employee(self):
        response = self.client.get('/api/employee/1')
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/employee/10')
        self.assertEqual(404, response.status_code)

    def test_get_all_employees(self):
        response = self.client.get('/api/employee')
        self.assertEqual(200, response.status_code)

    def test_put_employee(self):
        response = self.client.put('api/employee/1', json={'name': 'Will'})
        self.assertEqual(201, response.status_code)

        check = self.client.get('api/employee/1')
        check_decoded = check.data.decode()
        self.assertTrue('Will' in check_decoded)

        response = self.client.put('api/employee/1', json={'foo': 'bar'})
        self.assertEqual(400, response.status_code)

        response = self.client.put('api/employee/10', json={'name': 'Will'})
        self.assertEqual(404, response.status_code)

    def test_delete_employee(self):
        response = self.client.delete('api/employee/2')
        self.assertEqual(200, response.status_code)

        response = self.client.delete('api/employee/10')
        self.assertEqual(404, response.status_code)

    def test_post_employee(self):
        response = self.client.post('api/employee', json=self.EMP_JSON)
        self.assertEqual(201, response.status_code)

        check = self.client.get('api/employee')
        check_decoded = check.data.decode()
        self.assertTrue('Vova' in check_decoded)

        response = self.client.post('api/employee', json={'foo': 'bar'})
        self.assertEqual(400, response.status_code)

        response = self.client.post('api/employee', json={'name': ''})
        self.assertEqual(404, response.status_code)


if __name__ == "__main__":
    main()
