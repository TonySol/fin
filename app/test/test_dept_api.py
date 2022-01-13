from app.test import TestBase
from unittest import main

from app import db
from app.models.model import Department


class TestAPI(TestBase):
    DEPT_JSON = {"name": "Added"}

    @classmethod
    def setUp(cls):
        """Populates DB with required data"""
        super().setUp()

        dept1 = Department(name="DeptOne")
        dept2 = Department(name="DeptDelete")
        db.session.add(dept1)
        db.session.add(dept2)

        db.session.commit()

    def test_get_department(self):
        response = self.client.get('/api/department/1')
        self.assertEqual(200, response.status_code)

        response = self.client.get('/api/department/10')
        self.assertEqual(404, response.status_code)

    def test_get_all_departments(self):
        response = self.client.get('/api/department')
        self.assertEqual(200, response.status_code)

    def test_put_department(self):
        response = self.client.put('api/department/1', json={'name': 'Renamed'})
        self.assertEqual(201, response.status_code)

        check = self.client.get('api/department/1')
        check_decoded = check.data.decode()
        self.assertTrue('Renamed' in check_decoded)

        response = self.client.put('api/department/1', json={'foo': 'bar'})
        self.assertEqual(400, response.status_code)

        response = self.client.put('api/department/10', json={'name': 'Renamed'})
        self.assertEqual(404, response.status_code)

    def test_delete_department(self):
        response = self.client.delete('api/department/2')
        self.assertEqual(200, response.status_code)

        response = self.client.delete('api/department/10')
        self.assertEqual(404, response.status_code)

    def test_post_department(self):
        response = self.client.post('api/department', json=self.DEPT_JSON)
        self.assertEqual(201, response.status_code)

        check = self.client.get('api/department')
        check_decoded = check.data.decode()
        self.assertTrue('Added' in check_decoded)

        response = self.client.post('api/department', json={'foo': 'bar'})
        self.assertEqual(400, response.status_code)

        response = self.client.post('api/department', json={'name': '124'})
        self.assertEqual(404, response.status_code)


if __name__ == "__main__":
    main()
