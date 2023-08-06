from __future__ import annotations
from dataclasses import dataclass

from enum import Enum
from multiprocessing.connection import Client
from typing import Any, Dict, List, Optional

from strangeworks.transport.gql_client import StrangweorksGQLClient, Operation


@dataclass
class Resource:
    id: str
    slug: str
    status: str
    name: str
    product_slug: str
    product_name: str
    api_route: str

    @classmethod
    def from_dict(cls, d: dict):
        return Resource(
            id=d["id"],
            slug=d["slug"],
            status=d["status"],
            name=d["name"],
            product_slug=d["product"]["slug"],
            product_name=d["product"]["name"],
            api_route=d["product"]["apiRoute"],
        )


fetch_resource = Operation(
    query="""
        query getWorkspaceResource($workspaceSlug: String!, $resourceSlug: String!) {
            workspace(slug: $workspace_slug) {
               resource(resourceSlug: $resource_slug) {
                    slug
                    status
                    name
                    product {
                        slug
                        name
                        apiRoute                    
                    }
                }
            }
        }
        """
)


def fetch_resource(
    client: StrangweorksGQLClient,
    resource_slug: str,
    workspace_slug: str = None,
) -> Resource:
    """Retrieve a list of available resources.
    Parameters
    ----------
    status_list: Optional(List[str])
        retrieve only those resources whose status is included in this list.
    """
    if workspace_slug is None:
        workspace_slug = client.workspace_slug()
    result = client.execute(op=fetch_resource, **locals())
    return Resource.from_dict(result["resource"])
