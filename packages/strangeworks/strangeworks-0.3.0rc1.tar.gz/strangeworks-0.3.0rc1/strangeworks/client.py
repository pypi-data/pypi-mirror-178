"""client.py."""
from dataclasses import dataclass
import importlib.metadata
import os
import resource
from typing import Dict, List, Optional
from strangeworks.transport.backends import Backend, get_backend, get_backends

from strangeworks.config.base import ConfigSource
from strangeworks.transport.jobs import Job
from strangeworks.transport.auth import StrangeworksAuthenticator
from strangeworks.transport.rest_client import StrangeworksRestClient
from strangeworks.transport.gql_client import StrangweorksGQLClient
from strangeworks.transport.jobs import get_job
from strangeworks.transport.resources import Resource, fetch_resource
from strangeworks.errors.error import StrangeworksError

__version__ = importlib.metadata.version("strangeworks")


class Client:
    """Strangeworks client object."""

    def __init__(
        self,
        cfg: ConfigSource,
        resource_slug: str = None,
        headers: Optional[Dict[str, str]] = None,
        rest_client: Optional[StrangeworksRestClient] = None,
        gql_client: Optional[StrangweorksGQLClient] = None,
        **kwargs,
    ) -> None:
        """Strangeworks client.

        Implements the Strangeworks API and provides core functionality for cross-vendor
        applications.

        Parameters
        ----------
        cfg: ConfigSource
            Source for retrieving SDK configuration values.
        headers : Optional[Dict[str, str]]
            Headers that are sent as part of the request to Strangeworks.
        rest_client : Optional[StrangeworksRestClient]
        **kwargs
            Other keyword arguments to pass to tools like ``requests``.
        """
        self.cfg = cfg
        self.kwargs = kwargs

        self.headers = (
            os.getenv("STRANGEWORKS_HEADERS", default=None)
            if headers is None
            else headers
        )

        api_key = self.cfg.get("api_key")
        url = self.cfg.get("url")

        if rest_client is not None:
            self.rest_client = rest_client
        else:
            self.rest_client = StrangeworksRestClient(
                host=url,
                api_key=api_key,
                headers=self.headers,
                version=__version__,
                **self.kwargs,
            )

        if gql_client is not None:
            self.gql_client = gql_client
        else:
            self.gql_client = StrangweorksGQLClient(
                api_key=api_key,
                base_url=url,
            )

        if resource_slug is not None:
            self.select_resource(resource_slug)

    def authenticate(
        self,
        api_key: Optional[str] = None,
        url: Optional[str] = None,
        profile: Optional[str] = None,
        store_credentials: bool = True,
        overwrite: bool = False,
        **kwargs,
    ) -> None:
        """Authenticate to Strangeworks.

        Authenticate is used to generate an auth token and utilized within the session
        with the api_key. Will overwrite an auth token that is stored
        either in configuration or memory when called

        Parameters
        ----------
        api_key : Optional[str]
            The API key.
        url: Optional[str]
            The base URL to the Strangeworks API.
        **kwargs
            Other keyword arguments to pass to the ``StrangeworksRestClient`` object.
        """
        authenticator = StrangeworksAuthenticator(api_key=api_key)
        authenticator.authenticate()

        # create new clients w/ auth in place
        self.rest_client = StrangeworksRestClient(authenticator=authenticator)
        self.gql_client = StrangweorksGQLClient(authenticator=authenticator)

        # if we made it this far, lets go ahead and try to save the file
        if store_credentials:
            self.cfg.set(
                profile=profile,
                overwrite=overwrite,
                api_key=api_key,
                url=self.rest_client.get_host(),
            )

    def select_resource(self, resource_slug: str) -> None:
        selected_resource = fetch_resource(
            self.gql_client, self.workspace_slug, self.resource_slug
        )
        self.selected_resource = selected_resource

    def fetch_job(self, job_id: str, resource_id: str = None) -> Job:
        """Fetch the given ``job_id`` from the Strangeworks platform.

        Parameters
        ----------
        job_id : str

        Returns
        -------
        : Job
            The ``Job`` object.

        See Also
        --------
        strangeworks.jobs.jobs
        """

        return get_job(self.gql_client, job_id)

    def send_proxy_request(
        self,
        route: str,
        no_resource: bool = False,
        expected_response: int = 200,
        json: Optional[dict] = None,
        files: Optional[dict] = None,
        selected_resource: Resource = None,
        product_slug: str = None,
    ) -> dict:
        """
        Sends a request to the Strangeworks Product Proxy allowing
        communication with a Strangeworks Product or Workspace Resource.
        Returns the json body of the response.
        """

        if no_resource:
            if product_slug is None:
                raise StrangeworksError.user_error(
                    message=(
                        "Missing product_slug. Must include product_slug to contact proxy when not providing resource"
                    )
                )
            url = f"{self._host}/product/{product_slug}/{route}"

        else:
            # override resource if one is provided and ensure
            # one has been selected
            if selected_resource is None:
                selected_resource = self.selected_resource
            if selected_resource is None:
                raise StrangeworksError.user_error(
                    message=(
                        "Missing selected_resource. Use "
                        "strangeworks.select_resource(resource_slug), or provide one in this method and try again."
                    )
                )
            url = f"{self._host}/product/{product_slug}/resource/{selected_resource.slug}/{route}"

        return self.rest_client.post(
            url,
            expected_response=expected_response,
            json=json,
            files=files,
        )

    def get_backends(
        self,
        product_slugs: List[str] = None,
        backend_type_slugs: List[str] = None,
        backend_statuses: List[str] = None,
        backend_tags: List[str] = None,
    ) -> List[Backend]:
        """
        Returns a list of backends available based on the filters provided.
        Replaces the deprecated BackendsService
        """
        return get_backends(self.gql_client, **locals())

    def get_backend(self, backend_slug: str) -> Backend:
        """
        Returns a single backend by the slug.
        Replaces the deprecated BackendsService.
        """
        return get_backend(self.gql_client, backend_slug)

    def _host(self, new_host: Optional[str] = None) -> None:
        """Assign a new host to the ``StrangeworksRestClient`` object.

        Parameters
        ----------
        new_host : Optional[str]

        Returns
        -------
        None
        """
        self.__host = new_host
        rc = StrangeworksRestClient(
            host=new_host,
            headers=self.headers,
            **self.kwargs,
        )
        self.rest_client = rc
        self.backends_service._new_client(self.rest_client)
        self.circuit_runner._new_client(self.rest_client)
