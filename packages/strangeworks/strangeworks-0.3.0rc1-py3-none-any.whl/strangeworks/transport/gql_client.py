"""platform.py."""
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from gql import Client, gql
from gql.transport.exceptions import TransportQueryError

import requests
from gql.transport.requests import RequestsHTTPTransport
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RequestException

from strangeworks.errors.error import StrangeworksError
from strangeworks.transport.auth import StrangeworksAuthenticator


DEFAULT_PLATFORM_BASE_URL = "https://api.strangeworks.com"
PLATFORM_SERVICES_PATH = "services"


ALLOWED_HEADERS = {""}


class Operation:
    """Object for definining requests made to the platform."""

    def __init__(
        self,
        query: str,
        allowed_vars: Optional[List[str]] = None,
        upload_files: bool = False,
    ) -> None:
        """Initialize object

        Accepts a GraphQL query or mutation as a string. Derives variable names used by
        the query if none were provided.

        Parameters
        ----------
        query: str
            a GraphQL query or mutation as string.
        allowed_vars: Optional[List[str]]
            list to override which variables can be sent was part of query.
        """
        self.query = gql(query)
        self.allowed_vars = (
            allowed_vars
            if allowed_vars
            else list(
                map(
                    lambda x: x.variable.name.value,
                    self.query.definitions[0].variable_definitions,
                )
            )
        )
        self.upload_files = upload_files

    def variables(
        self, values: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:

        if not self.allowed_vars:
            return values

        vars = {}
        for k, v in values.items():
            if k in self.allowed_vars and v is not None:
                vars[k] = v
        return vars


class StrangeworksTransport(RequestsHTTPTransport):
    """Transport layer with automatic token refresh."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        platform_url: str = "platform",
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        authenticator: Optional[StrangeworksAuthenticator] = None,
        retries: int = 0,
        **kvargs,
    ) -> None:
        self.platform_url = urljoin(base_url, platform_url)
        self.auth_url = urljoin(base_url, "service/token")
        self.api_key = api_key
        self.authenticator = authenticator

        if self.authenticator is None:
            self.authenticator = StrangeworksAuthenticator()

        super().__init__(
            url=self.platform_url,
            headers=headers,
            timeout=timeout,
            retries=retries,
        )
        self.auth_token: Optional[str] = None

    def connect(self):
        """Set up a session object.

        Creates a session object for the transport to use and configures retries and
        re-authentication.
        """
        if self.session is None:

            self.session = requests.Session()

            # set up retries.
            if self.retries > 0:
                adapter = HTTPAdapter(
                    max_retries=Retry(
                        total=self.retries,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504],
                        allowed_methods=None,
                    )
                )

                for prefix in "http://", "https://":
                    self.session.mount(prefix, adapter)

            # setup token refresh if expired.
            self.session.hooks["response"].append(self._reauthenticate)

        if self.auth_token is None:
            self.authenticator.authenticate(self.api_key)
            if self.headers:
                self.headers["Authorization"] = self.authenticator.auth_token()
            else:
                self.headers = {"Authorization": self.authenticator.auth_token()}

    def _reauthenticate(self, res: requests.Response, **kwargs) -> requests.Response:
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
            self.authenticator.authenticate(self.api_key)
            if self.headers:
                self.headers["Authorization"] = self.authenticator.auth_token()
            else:
                self.headers = {"Authorization": self.authenticator.auth_token()}
            # self.session.send just sends the prepared request, so we must manually
            # ensure that the new token is part of the header
            res.request.headers["Authorization"] = f"Bearer {self.auth_token}"
            res.request.headers[seen_before_header] = True
            return self.session.send(res.request)


class StrangweorksGQLClient:
    """Client for Platform API."""

    def __init__(
        self,
        api_key: Optional[str],
        base_url: Optional[str] = None,
        auth_token: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        authenticator: Optional[StrangeworksAuthenticator] = None,
        timeout: Optional[int] = None,
        retries: int = 0,
    ) -> None:
        """Initialize platform API client.

        Provides access to the platform API methods which allows python SDK clients to interact
        with the Strangeworks platform.

        Parameters
        ----------
        auth_token: str
            jwt token used to authorize requests to the platform API's.
        platform_url: str
            Base url for accessing the platform API. Defaults to
            https://api.strangeworks.com
        headers: Dict[str, str]
            Additional values to set in the header for the request. The header must
            belong to ALLOWED_HEADERS.
        """
        self.platform_url = urljoin(
            base_url or DEFAULT_PLATFORM_BASE_URL, PLATFORM_SERVICES_PATH
        )

        self.gql_client = Client(
            transport=StrangeworksTransport(
                base_url=self.platform_url,
                api_key=api_key,
                authenticator=authenticator,
            )
        )

    def execute(self, op: Operation, **kvargs):
        """Execute an operation on the platform.
        Parameters
        ----------
        op: Operation
            which request to run
        variable_values; Optional[Dict[str, Any]]
            values to send with the request
        """
        try:
            result = self.gql_client.execute(
                document=op.query,
                variable_values=op.variables(kvargs),
                upload_files=op.upload_files,
            )
            return result
        except TransportQueryError as e:
            print(f"error during query: {e}")
            raise StrangeworksError.server_error(e)

    def workspace_slug(self) -> str:
        return self.gql_client.authenticator.workspace_slug()
