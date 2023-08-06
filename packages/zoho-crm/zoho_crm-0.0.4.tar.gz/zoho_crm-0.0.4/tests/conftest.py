import pytest

from zoho_crm import ZohoAuthConfig, ZohoClient


@pytest.fixture
def zoho_client():
    return ZohoClient(
        zoho_auth_config=ZohoAuthConfig(
            client_id="clientid",
            client_secret="clientsecret",
            refresh_token="refreshtoken",
        )
    )
