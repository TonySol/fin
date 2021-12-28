import unittest

from app import start_app, db
from config import Test
from app.models.model import Department, Employee
from app.service.services import DepartmentService, EmployeeService

class TestServices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = start_app(Test)
        # db.create_all(app=start_app(Test))
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        dept1 = Department(name="Test_dept1")
        dept2 = Department(name="Test_dept2")
        db.session.add(dept1)
        db.session.add(dept2)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()


    def test_get_by_prime_key(self):
        self.assertEqual(DepartmentService.get_by_prime_key("Test_dept1").name, "Test_dept1")
        self.assertEqual(DepartmentService.get_by_prime_key("Not Existing"), None)

    def test_delete_by_prime_key(self):
        DepartmentService.delete_by_prime_key("Test_dept2")
        result = db.session.query(Department).count()
        self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main()
