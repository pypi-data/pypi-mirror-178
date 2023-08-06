import pytest
from pytest_mock import MockerFixture
from requests_mock import Mocker

from zoho_crm import (
    ZohoAPIConfig,
    ZohoAuthConfig,
    ZohoClient,
    ZohoClientException,
    ZohoEndpoint,
)


class TestZohoAPIConfig:
    def test_api_base_url(self):
        assert ZohoAPIConfig().api_base_url == "https://www.zohoapis.eu/crm/v3/"


class TestZohoAuthConfig:
    def test_auth_base_url(self):
        assert (
            ZohoAuthConfig().auth_base_url == "https://accounts.zoho.eu/oauth/v2/token"
        )

    def test_refresh_access_token(self):
        assert ZohoAuthConfig(
            client_id="12345", client_secret="6789", refresh_token="token1"
        ).refresh_access_token_url == (
            "https://accounts.zoho.eu/oauth/v2/"
            "token?refresh_token=token1&client_id=12345&client_secret=6789&grant_type=refresh_token"
        )


class TestZohoEndpoint:
    @pytest.mark.parametrize(
        "file_type,params,expected",
        [
            (None, {"1": 1}, "patata"),
            ("photo", {"id": 1}, "patata/1/photo"),
            ("Attachments", {"id": 1}, "patata/1/Attachments"),
            (None, {"criteria": "something"}, "patata/search"),
        ],
    )
    def test_url(self, file_type: str, params: dict, expected: str):
        assert (
            ZohoEndpoint(
                module_name="patata", method="get", params=params, file_type=file_type
            ).url
            == expected
        )


class TestZohoClient:
    def test__init__no_params(self):
        zoho_client = ZohoClient()

        assert isinstance(zoho_client.zoho_config, ZohoAPIConfig)
        assert isinstance(zoho_client.zoho_auth, ZohoAuthConfig)

    def test__init__(self):
        zoho_client = ZohoClient(
            zoho_api_config=ZohoAPIConfig(), zoho_auth_config=ZohoAuthConfig()
        )

        assert isinstance(zoho_client.zoho_config, ZohoAPIConfig)
        assert isinstance(zoho_client.zoho_auth, ZohoAuthConfig)

    def test_validate_response_ok(self, zoho_client: ZohoClient):
        assert zoho_client._validate_response({"patata": 1}) == {"patata": 1}

    @pytest.mark.parametrize(
        "response",
        [({"error": 1}), ({"status": "error"}), ({"data": [{"status": "error"}]})],
    )
    def test_validate_response_error(self, response: dict):
        with pytest.raises(ZohoClientException):
            ZohoClient()._validate_response(response)

    def test__get_new_access_token_KO(
        self, zoho_client: ZohoClient, requests_mock: Mocker
    ):
        requests_mock.post(
            zoho_client.zoho_auth.refresh_access_token_url, json={"error": "error 1"}
        )

        with pytest.raises(ZohoClientException):
            zoho_client._get_new_access_token()

    def test__get_new_access_token_OK(
        self, zoho_client: ZohoClient, requests_mock: Mocker
    ):
        requests_mock.post(
            zoho_client.zoho_auth.refresh_access_token_url,
            json={"access_token": "AA1234"},
        )

        assert zoho_client._get_new_access_token() == "AA1234"

    def test_request_headers_not_cached(
        self, zoho_client: ZohoClient, mocker: MockerFixture, requests_mock: Mocker
    ):
        requests_mock.post(
            zoho_client.zoho_auth.refresh_access_token_url,
            json={"access_token": "AA1234"},
        )
        spy__get_new_access_token = mocker.patch.object(
            zoho_client,
            "_get_new_access_token",
            wraps=zoho_client._get_new_access_token,
        )

        returned_headers = zoho_client.request_headers

        spy__get_new_access_token.assert_called_once()
        assert zoho_client._request_headers == {
            "Authorization": "Zoho-oauthtoken AA1234"
        }
        assert returned_headers == {"Authorization": "Zoho-oauthtoken AA1234"}

    def test_request_headers_already_cached(self, zoho_client: ZohoClient):
        zoho_client._request_headers = {"example": "example"}

        assert zoho_client.request_headers == {"example": "example"}

    def test__get_next_page_url_no_more(self, zoho_client: ZohoClient):
        page_info = {"more_records": False}
        next_page = zoho_client._get_next_page_url(page_info, {"page": 5})

        assert next_page is False

    def test__get_next_page_url_with_page_token(self, zoho_client: ZohoClient):
        params = {"page": 1}
        page_info = {
            "page": 3000,
            "more_records": True,
            "per_page": 2000,
            "next_page_token": "fakenextpagetoken1",
        }
        next_page = zoho_client._get_next_page_url(page_info, params)

        assert next_page is True
        assert "page" not in params
        assert params["page_token"] == "fakenextpagetoken1"

    def test__get_next_page_url_with_page_number(self, zoho_client: ZohoClient):
        params = {"page": 1}
        page_info = {"page": 1, "more_records": True, "per_page": 2}

        next_page = zoho_client._get_next_page_url(page_info, params)

        assert params["page"] == 2
        assert next_page

    def test__get_page_without_next_url(
        self, zoho_client: ZohoClient, requests_mock: Mocker
    ):
        zoho_endpoint = ZohoEndpoint(module_name="testmodule", method="get")
        zoho_client._request_headers = {"authorization": "fake"}
        fake_response = {
            "info": {"more_records": False},
            "data": [{"example": "example"}],
        }
        requests_mock.get(
            "https://www.zohoapis.eu/crm/v3/testmodule", json=fake_response
        )

        response_data, next_url = zoho_client._get_page(zoho_endpoint)

        assert response_data == [{"example": "example"}]
        assert not next_url

    def test__get_page_with_next_url(
        self, zoho_client: ZohoClient, requests_mock: Mocker
    ):
        zoho_endpoint = ZohoEndpoint(module_name="testmodule", method="get")
        zoho_client._request_headers = {"authorization": "fake"}
        requests_mock.get(
            "https://www.zohoapis.eu/crm/v3/testmodule",
            json={
                "info": {"more_records": True, "page": 1, "per_page": 2},
                "data": [{"example": "example"}],
            },
        )

        response_data, next_url = zoho_client._get_page(zoho_endpoint)

        assert response_data == [{"example": "example"}]
        assert next_url

    def test__get_page_json_decode_error(
        self, zoho_client: ZohoClient, requests_mock: MockerFixture
    ):
        zoho_endpoint = ZohoEndpoint(module_name="testmodule", method="get")
        zoho_client._request_headers = {"authorization": "fake"}
        requests_mock.get(
            "https://www.zohoapis.eu/crm/v3/testmodule",
            text="...",
        )

        response_data, next_url = zoho_client._get_page(zoho_endpoint)

        assert response_data == []
        assert not next_url

    def test__call_read_endpoint(self, zoho_client: ZohoClient, mocker: MockerFixture):
        mocker.patch(
            "zoho_crm.ZohoClient._get_page",
            side_effect=[([1, 2], True), ([3, 4], False)],
        )
        zoho_endpoint = ZohoEndpoint(module_name="testmodule", method="get")

        assert zoho_client._call_read_endpoint(zoho_endpoint) == [1, 2, 3, 4]

    def test__call_write_endpoint(self, zoho_client: ZohoClient, requests_mock: Mocker):
        requests_mock.post(
            "https://www.zohoapis.eu/crm/v3/testmodule",
            json={"response": "OK"},
        )
        zoho_client._request_headers = {"authorization": "fake"}
        zoho_endpoint = ZohoEndpoint(module_name="testmodule", method="post")

        assert zoho_client._call_write_endpoint(zoho_endpoint) == {"response": "OK"}

    def test__call_write_endpoint_json_decode_error(
        self, zoho_client: ZohoClient, requests_mock: Mocker
    ):
        requests_mock.post(
            "https://www.zohoapis.eu/crm/v3/testmodule",
            text="...",
        )
        zoho_client._request_headers = {"authorization": "fake"}
        zoho_endpoint = ZohoEndpoint(module_name="testmodule", method="post")

        assert zoho_client._call_write_endpoint(zoho_endpoint) == {}

    @pytest.mark.parametrize(
        "mock_address,method",
        [
            ("zoho_crm.ZohoClient._call_read_endpoint", "get"),
            ("zoho_crm.ZohoClient._call_write_endpoint", "post"),
        ],
    )
    def test_call(
        self,
        zoho_client: ZohoClient,
        mocker: MockerFixture,
        mock_address: str,
        method: str,
    ):
        mock_endpoint = mocker.patch(mock_address)
        zoho_endpoint = ZohoEndpoint(module_name="testmodule", method=method)

        zoho_client.call(zoho_endpoint)

        mock_endpoint.assert_called_with(zoho_endpoint)
