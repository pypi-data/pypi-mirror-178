from eve.auth import TokenAuth
from flask import current_app as app

from .verifier import AzureVerifier


class AzureAuth(TokenAuth):

    def get_configs(self):
        tenant = app.config.get('AZURE_AD_TENANT')
        issuer = app.config['AZURE_AD_ISSUER']
        audiences = app.config['AZURE_AD_AUDIENCES']

        return dict(tenant=tenant, issuer=issuer, audiences=audiences)

    def validate_token(self, token):
        return AzureVerifier(**self.get_configs()).verify(token)

    def check_auth(self, token, allowed_roles, resource, method):
        return self.validate_token(token)
