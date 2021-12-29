import http
import os
import tempfile
from unittest import TestCase, main

from config import Test
from app import start_app, db

class TestWebViews(TestCase):
    @classmethod
    def setUpClass(cls):
        """Makes a test db in temp file, populates it and pushes app context"""
        cls.file_handle, cls.file_path = tempfile.mkstemp()
        Test.SQLALCHEMY_DATABASE_URI = f'sqlite:///{cls.file_path}'

        cls.app = start_app(Test)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        cls.client = cls.app.test_client()


    @classmethod
    def tearDownClass(cls):
        """Removes db by closing link to the temp file, and removes app context"""
        db.session.remove()
        os.close(cls.file_handle)
        os.unlink(cls.file_path)

        cls.app_context.pop()

    def test_departments(self):
        response = self.client.get('/departments')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

if __name__ == "__main__":
    main()