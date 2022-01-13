import os
import tempfile

from unittest import TestCase

from config import Test
from app import start_app, db


class TestBase(TestCase):

    @classmethod
    def setUp(cls):
        """Makes a test db in temp file, populates it and pushes app context

        creates a test client, which allows to preserve a request context after request was handled
        this helps get all request execution details for tests,
        """
        cls.file_handle, cls.file_path = tempfile.mkstemp()
        Test.SQLALCHEMY_DATABASE_URI = f'sqlite:///{cls.file_path}'

        cls.app = start_app(Test)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        cls.client = cls.app.test_client()

        db.create_all()

    @classmethod
    def tearDown(cls):
        """Removes db by closing link to the temp file, and removes app context

        Call destruction of request and app context manually, because test_client blocks the
        automatic stack clean up. Or unittest will leak memory."""
        db.session.remove()
        os.close(cls.file_handle)
        os.unlink(cls.file_path)

        cls.app_context.pop()