"""rest_client.py."""
import warnings
from typing import Dict, Optional

import requests

from strangeworks.config.defaults import DEFAULT_URL
from strangeworks.errors.error import StrangeworksError


class StrangeworksAuthenticator:
    """
    Strangeworks shared authentication class.
    Utilized for handling auth in either the GQL or REST API interfaces.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        host: Optional[str] = None,
    ):
        self.__api_key = api_key
        self.__host = host
        if host is None:
            self.__host = DEFAULT_URL

    def authenticate(
        self,
        api_key: Optional[str] = None,
        host: Optional[str] = None,
        **kwargs,
    ):
        """Authenticate to Strangeworks.
        Returns the payload returned by Strangeworks

        Parameters
        ----------
        api_key : Optional[str]
            The API key.
        host: Optional[str]
            The base URL to the Strangeworks API.
        **kwargs
            Other arguments to be passed to ``requests``.
        """
        if host is not None and host != "":
            self.__host = host

        # if no api key was passed in ensure an existing api key
        # exists for reauthentication. throw an error if neither is provided.
        if api_key is None:
            if self.__api_key is None:
                raise StrangeworksError.authentication_error(
                    message=(
                        "Missing api_key. Use "
                        "strangeworks.authenticate(api_key) and try again."
                    ),
                )
            else:
                api_key = self.__api_key

        # Exchange api key for token to use with local SDK requests
        url = f"{self.__host}/user/token"
        self.headers["x-strangeworks-api-key"] = api_key
        request_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key in self.ALLOWED_REQUEST_KWARGS
        }
        res = requests.post(
            url,
            json={},
            headers=self.headers,
            **request_kwargs,
        )
        if not res.ok:
            raise StrangeworksError.authentication_error(
                f"Error getting token: {res.status_code} text: {res.text} URL: {url}"
            )
        if res.ok:
            print("Successfully connected to Strangeworks, happy computing!")
        response = res.json()

        # store valid authentication vars for use by clients
        self.__api_key = api_key
        self.__auth_token = response["accessToken"]
        self.__workspace_slug = response["workspaceSlug"]

    def workspace_slug(self) -> str:
        return self.__workspace_slug

    def auth_token(self) -> str:
        return self.__auth_token
