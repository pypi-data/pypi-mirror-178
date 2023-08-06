"""rest_client.py."""
import warnings
from typing import Dict, Optional

import requests

from strangeworks.config.defaults import DEFAULT_URL
from strangeworks.errors.error import StrangeworksError
from strangeworks.transport.auth import StrangeworksAuthenticator


class StrangeworksRestClient:
    """Strangeworks REST client."""

    ALLOWED_REQUEST_KWARGS = [
        "params",
        "data",
        "json",
        "headers",
        "cookies",
        "files",
        "auth",
        "timeout",
        "allow_redirects",
        "proxies",
        "verify",
        "stream",
        "cert",
    ]

    def __init__(
        self,
        headers: Optional[Dict[str, str]] = None,
        host: Optional[str] = None,
        api_key: Optional[str] = None,
        auth_token: Optional[str] = None,
        session: Optional[requests.Session] = None,
        default_timeout: Optional[int] = None,
        authenticator: Optional[StrangeworksAuthenticator] = None,
        version: str = "",
        **kwargs,
    ) -> None:
        """Strangeworks REST client.

        Parameters
        ----------
        headers : Optional[Dict[str, str]]
            Headers that are sent as part of the request to Strangeworks.
        host : Optional[str]
            The host URL. Defaults to https://api.quantumcomputing.com.
        api_key : Optional[str]
            A secret api_key that can be accessed on quantumcomputing.com.
        auth_token : Optional[str]
            A JWT token used for authorization.
        session : Optional[requests.Session]
            A user defined session object to use.
        default_timeout : Optional[int]
            Timeout in milliseconds before timing out a request.
        version : str, optional, default is ""
            The version of the Strangeworks client being used.
        **kwargs
            Other keyword arguments to pass to tools like ``requests``.

        See Also
        --------
        strangeworks.client.Client
        """
        self.kwargs = kwargs
        self.__auth_token = auth_token
        self.__default_timeout = default_timeout
        if headers is None:
            self.headers = {
                "X-Strangeworks-API-Version": "0",
                "X-Strangeworks-Client-ID": "strangeworks-sdk-python",
                "X-Strangeworks-Client-Version": version,
                "x-strangeworks-provider-account": "",
                "Authorization": f"Bearer {auth_token}",
            }

        self.__host = host
        if host is None:
            self.__host = DEFAULT_URL

        if session is None:
            self.__session = self.create_session()
        elif session is not None:
            if not isinstance(session, requests.Session):
                message = (
                    f"The given session object ({session}) is not a valid "
                    "requests.Session object. Reverting to a new requests.Session "
                    "object."
                )
                warnings.warn(message, UserWarning)
                self.__session = self.create_session()
            else:
                self.__session = session

        self.__session.headers.update(self.headers)
        # set up re-authentication hook!
        self.__session.hooks["response"].append(self.__reauthenticate)

        self.__authenticator = authenticator
        if self.__authenticator is None:
            self.__authenticator = StrangeworksAuthenticator()

        # if a user has passed in authentication vars but has not generated a token
        # do so now, otherwise pass along
        if self.__auth_token is None and api_key is not None:
            self.__authenticator.authenticate(api_key, **self.kwargs)

    def create_session(self) -> requests.Session:
        """Create a ``requests.Session`` object for interacting with Strangeworks.

        Returns
        -------
        session : requests.Session
            The session object created by requests.
        """
        session = requests.Session()
        # Add any keyword arguments to the session if the session object has that
        # attribute.
        for key, value in self.kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        return session

    def post(
        self,
        url: str = "",
        json: Optional[dict] = None,
        files: Optional[dict] = None,
        expected_response: int = 200,
    ) -> dict:
        """Send a POST command to the given URL endpoint.

        Parameters
        ----------
        url : str, optional, default is ""
            The URL to send the POST command to.
        json : Optional[dict]
            Not a real JSON object, but a Python dictionary that can be serialized to
            JSON.
        files : Optional[dict]
            A Python dictionary of files, can be used for multipart uploads.
        expected_response : int, optional, default is ``200``
            The expected response from the endpoint.

        Returns
        -------
        res : dict
            The result from the POST command.

        See Also
        --------
        requests.request
        """
        self.__session.headers.update(self.headers)
        r = self.__session.post(
            url=f"{self.__host}{url}",
            json=json,
            files=files,
            timeout=self.__default_timeout,
        )
        if r.status_code != expected_response:
            self.__parse_error(r)
        # NOTE: If there is no JSON serializable object, then this will result in an
        #       error.
        res = r.json()
        return res

    def delete(self, url: str = "", expected_response: int = 200) -> None:
        """Issue a DELETE request to the given URL.

        Parameters
        ----------
        url : str
            The endpoint to delete.
        expected_response : int, optional, default is ``200``
            The expected response from the endpoint.
        """
        self.__session.headers.update(self.headers)
        # XXX: We should give the user feedback when issuing this command.
        r = self.__session.delete(
            url=f"{self.__host}{url}",
            timeout=self.__default_timeout,
        )
        if r.status_code != expected_response:
            self.__parse_error(r)

    def get(self, url: str = "") -> dict:
        """Use the session to issue a GET.

        Parameters
        ----------
        url : str
            The URL to perform the GET request.

        Returns
        -------
        res : dict
            The JSON response.
        """
        self.__session.headers.update(self.headers)
        r = self.__session.get(url=f"{self.__host}{url}")
        if r.status_code != 200:
            self.__parse_error(r)
        # NOTE: If there is no JSON serializable object, then this will result in an
        #       error.
        res = r.json()
        return res

    def authenticate(
        self,
        api_key: Optional[str] = None,
        host: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.__authenticator.authenticate(**locals())
        self.__session.auth = self.__StrangeworksAuth(
            token=self.__authenticator.auth_token()
        )

    def get_host(self) -> str:
        """Return host/base url."""
        return self.__host

    def __reauthenticate(self, res: requests.Response, **kwargs) -> requests.Response:
        """Reauthenticate to Strangeworks.

        Parameters
        ----------
        res : requests.Response
        **kwargs

        Returns
        -------
        : requests.Response
        """
        if res.status_code == requests.codes.unauthorized:
            seen_before_header = "X-SW-SDK-Re-Auth"
            # We've tried once before but no luck. Maybe they've changed their api_key?
            if res.request.headers.get(seen_before_header):
                raise StrangeworksError(
                    "Unable to re-authenticate your request. Utilize "
                    "strangeworks.authenticate(api_key) with your most up "
                    "to date credentials and try again."
                )
            self.__authenticator.authenticate(**kwargs)
            self.__session.auth = self.__StrangeworksAuth(
                token=self.__authenticator.auth_token()
            )
            # self.session.send just sends the prepared request, so we must manually
            # ensure that the new token is part of the header
            res.request.headers["Authorization"] = f"Bearer {self.__auth_token}"
            res.request.headers[seen_before_header] = True
            return self.__session.send(res.request)

    def __parse_error(self, response: requests.Response) -> None:
        """Parse specific responses to a more human readable format.

        Parameters
        ----------
        response : requests.Response
            The response object from ``requests``.
        """
        error_payload = response.json()
        if "message" in error_payload and error_payload["message"] != "":
            raise StrangeworksError.bad_response(error_payload["message"])
        raise StrangeworksError.bad_response(
            f"Error status code: {response.status_code} text: {response.text}"
        )

    class __StrangeworksAuth(requests.auth.AuthBase):
        """Authenticate to Strangeworks.

        StrangeworksAuth is used to authenticate requests to the Strangeworks
        server. Token used may be a regular Strangeworks auth token (same one
        used for API's, etc.) or a token obtained using the api key which is
        limited in scope.
        """

        def __init__(self, token: Optional[str] = None) -> None:
            self.token = token

        def __call__(self, req: requests.Request) -> requests.Request:
            if self.token is None:
                raise StrangeworksError(
                    message=(
                        "No authentication method detected. Utilize "
                        "strangeworks.authenticate(api_key) and try again"
                    ),
                )
            # utilize the authorization header with bearer token
            req.headers["Authorization"] = f"Bearer {self.token}"
            return req
