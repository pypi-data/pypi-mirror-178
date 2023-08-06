from unittest import TestCase

from src.jwksutils import ensure_bytes


class TestEnsureBytes(TestCase):

    def test_should_return_bytes_when_is_str(self):
        self.assertEqual(ensure_bytes('asdf'), b'asdf')

    def test_should_return_bytes_when_is_not_str(self):
        self.assertEqual(ensure_bytes(b'asdf'), b'asdf')
