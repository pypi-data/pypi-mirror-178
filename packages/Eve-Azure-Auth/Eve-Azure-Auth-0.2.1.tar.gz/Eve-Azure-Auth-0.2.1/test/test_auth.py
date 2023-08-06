from unittest import TestCase
from unittest.mock import MagicMock, patch

from src import AzureAuth
from src.verifier import AzureVerifier


class TestAzureAuthCheckAuth(TestCase):

    @patch.object(AzureAuth, 'validate_token')
    def test_should_call_validate_token(self, validate_token_mock):
        AzureAuth().check_auth('asdf', None, None, None)
        validate_token_mock.assert_called_once_with('asdf')


class TestAzureAuthValidateToken(TestCase):

    @patch.object(AzureAuth, 'get_configs', MagicMock())
    @patch.object(AzureVerifier, 'verify')
    def test_should_call_auth_verifier(self, verify_mock):
        AzureAuth().validate_token('asdf')
        verify_mock.assert_called_once_with('asdf')
