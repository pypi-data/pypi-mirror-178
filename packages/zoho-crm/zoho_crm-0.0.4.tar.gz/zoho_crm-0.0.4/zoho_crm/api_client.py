import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple

import requests

logger = logging.getLogger(__name__)


class ZohoClientException(Exception):
    """handler errors from Zoho api"""


@dataclass
class ZohoAPIConfig:
    api_version: str = "v3"
    account_domain: str = "www.zohoapis.eu"
    api_results_per_page: int = 200
    api_discrete_pagination_limit: int = 2000

    @property
    def api_base_url(self) -> str:
        return f"https://{self.account_domain}/crm/{self.api_version}/"


@dataclass
class ZohoAuthConfig:
    client_id: str = os.environ.get("ZOHO_CLIENT_ID")
    client_secret: str = os.environ.get("ZOHO_CLIENT_SECRET")
    refresh_token: str = os.environ.get("ZOHO_REFRESH_TOKEN")
    auth_api_version: str = "v2"
    account_domain: str = "accounts.zoho.eu"

    @property
    def auth_base_url(self) -> str:
        return f"https://{self.account_domain}/oauth/{self.auth_api_version}/token"

    @property
    def refresh_access_token_url(self) -> str:
        return (
            f"{self.auth_base_url}?"
            f"refresh_token={self.refresh_token}&"
            f"client_id={self.client_id}&"
            f"client_secret={self.client_secret}&"
            f"grant_type=refresh_token"
        )


class FileTypes(Enum):
    PHOTO = "photo"
    ATTACHMENT = "Attachments"


@dataclass
class ZohoEndpoint:
    module_name: str
    method: str
    response_data_key: str = "data"
    file_type: FileTypes = None
    params: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)
    files: dict = field(default_factory=dict)

    @property
    def url(self):
        if "id" in self.params:
            record_url = f"{self.module_name}/{self.params['id']}"
            if self.file_type is not None:
                record_url = f"{record_url}/{self.file_type}"
            return record_url
        if "criteria" in self.params:
            return f"{self.module_name}/search"
        return self.module_name


class ZohoClient:
    def __init__(
        self,
        zoho_api_config: ZohoAPIConfig = None,
        zoho_auth_config: ZohoAuthConfig = None,
    ):
        self.zoho_config = zoho_api_config if zoho_api_config else ZohoAPIConfig()
        self.zoho_auth = zoho_auth_config if zoho_auth_config else ZohoAuthConfig()

    def _validate_response(self, response: Dict) -> Dict:
        if "error" in response or "error" == (
            response.get("status") or response.get("data", [{}])[0].get("status")
        ):
            raise ZohoClientException(f"The zoho server returned an error: {response}")
        return response

    def _get_new_access_token(self) -> str:
        """
        Renew the client access token and return the new one
        This action revoke the older ones
        """
        response_dict = requests.post(self.zoho_auth.refresh_access_token_url).json()
        response_dict = self._validate_response(response_dict)
        logger.debug("new access token got it: %s", response_dict)

        return response_dict["access_token"]

    @property
    def request_headers(self) -> str:
        try:
            return self._request_headers
        except AttributeError:
            token = self._get_new_access_token()
            self._request_headers = {"Authorization": f"Zoho-oauthtoken {token}"}
            return self._request_headers

    def _get_next_page_url(self, page_info: Dict, params: Dict) -> bool:
        if not page_info["more_records"]:
            return False

        amount = int(page_info["page"]) * page_info["per_page"]
        if amount >= self.zoho_config.api_discrete_pagination_limit:
            params["page_token"] = page_info["next_page_token"]
            params.pop("page", None)
            return True

        params["page"] = page_info["page"] + 1
        return True

    def _get_page(self, zoho_endpoint: ZohoEndpoint) -> Tuple[List[Dict], str | bool]:
        next_url = False
        try:
            response_dict = requests.get(
                self.zoho_config.api_base_url + zoho_endpoint.url,
                headers=self.request_headers,
                params=zoho_endpoint.params,
            ).json()
        except requests.exceptions.JSONDecodeError:
            return [], False

        valid_response_dict = self._validate_response(response_dict)
        if "info" in valid_response_dict:
            next_url = self._get_next_page_url(
                valid_response_dict["info"], zoho_endpoint.params
            )
        return valid_response_dict[zoho_endpoint.response_data_key], next_url

    def _call_read_endpoint(self, zoho_endpoint: ZohoEndpoint) -> List[Dict]:
        response_list = []

        next_page = True
        while next_page:
            result_list, next_page = self._get_page(zoho_endpoint)
            response_list.extend(result_list)

        return response_list

    def _call_write_endpoint(self, zoho_endpoint: ZohoEndpoint) -> Dict:
        try:
            response_dict = getattr(requests, zoho_endpoint.method)(
                self.zoho_config.api_base_url + zoho_endpoint.url,
                headers=self.request_headers,
                json=zoho_endpoint.data,
                files=zoho_endpoint.files,
            ).json()
        except requests.exceptions.JSONDecodeError:
            return {}
        valid_response_dict = self._validate_response(response_dict)
        return valid_response_dict

    def call(self, zoho_endpoint: ZohoEndpoint) -> Dict:
        if zoho_endpoint.method == "get":
            return self._call_read_endpoint(zoho_endpoint)
        return self._call_write_endpoint(zoho_endpoint)
