from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union

from strangeworks.errors.error import StrangeworksError
from strangeworks.transport.gql_client import Operation, StrangweorksGQLClient
from strangeworks.transport.rest_client import StrangeworksRestClient


@dataclass
class Backend:
    id: str
    data: dict
    data_schema: str
    name: str
    remote_backend_id: str
    remote_stauts: str

    @staticmethod
    def from_dict(backend: dict) -> Backend:
        id = backend.get("id", "")
        data = backend.get("data", {})
        data_schema = backend.get("dataSchema", "")
        name = backend.get("name", "")
        remote_backend_id = backend.get("remoteBackendId", "")
        remote_status = backend.get("remoteStatus", "")
        slug = backend.get("slug", {})
        return Backend(
            id=id,
            data=data,
            data_schema=data_schema,
            name=name,
            remote_backend_id=remote_backend_id,
            remote_status=remote_status,
            slug=slug,
        )

    def __repr__(self):
        return self.selector_id()

    def __str__(self):
        return self.selector_id()


get_backend_request = Operation(
    query="""
        query backend($slug: String!) {            
            backend(slug: $slug) {
                data,
                dataSchema,
                id,
                name,
                remoteBackendId,
                remoteStatus,
                slug,
            }
        }
    """
)


def get_backend(client: StrangweorksGQLClient, backend_slug: str) -> Backend:
    """
    Retrieve backend info
    """
    backend_response = client.execute(op=get_backend_request, **locals())
    return Backend.from_dict(backend_response["backend"])


get_backends_request = Operation(
    query="""
        query backends ($productSlugs: [String!], $backendTypeSlugs: [String!], $backendStatuses: [BackendStatus!], $backendTags: [String!]) {
                backends(productSlugs: $product_slugs, backendTypeSlugs: $backend_type_slugs, backendStatuses: $backend_statuses, backendTags: $backend_tags)
                    {
                        id,
                        name,
                        remoteBackendId,
                        remoteStatus,
                        slug,
                    }
                }        
    """
)


def get_backends(
    client: StrangweorksGQLClient,
    product_slugs: List[str] = None,
    backend_type_slugs: List[str] = None,
    backend_statuses: List[str] = None,
    backend_tags: List[str] = None,
) -> List[Backend]:
    """
    Retrieve a list of available backends. Does not fetch data to reduce
    size of payload.
    """
    backends_response = client.execute(
        op=get_backends_request,
        **locals(),
    )
    res = []
    for b in backends_response:
        res.append(Backend.from_dict(b["backend"]))
    return res
