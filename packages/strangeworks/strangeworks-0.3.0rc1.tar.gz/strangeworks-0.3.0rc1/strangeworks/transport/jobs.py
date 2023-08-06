import datetime
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from strangeworks.errors.error import StrangeworksError
from strangeworks.transport.gql_client import Operation, StrangweorksGQLClient


@dataclass
class File:
    id: str
    slug: Optional[str] = None
    label: Optional[str] = None
    file_name: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict):
        return File(
            id=d["id"],
            slug=d["slug"],
            label=d["label"],
            url=d["url"],
            file_name=d["fileName"],
        )


@dataclass
class Job:
    id: str
    child_jobs: Optional[List]
    service_identifier: Optional[str]
    slug: Optional[str]
    resource: Optional[Dict[str, Any]]
    status: Optional[str]
    is_terminal_state: Optional[str]
    remote_status: Optional[str] = None
    job_data_schema: Optional[str] = None
    job_data: Optional[Dict[str, Any]] = None
    files: Optional[List[File]] = None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(res: dict):
        child_jobs: List[Job] = []
        if "childJobs" in res:
            for _, child_job in res["childJobs"]:
                child_jobs.append(Job.from_dict(child_job))

        files: List[File] = []
        if "files" in res:
            for _, f in res["files"]:
                files.append(File.from_dict(f))

        return Job(
            id=res["id"],
            service_identifier=res["serviceIdentifier"],
            slug=res["slug"],
            resource=res["resource"] if "resource" in res else None,
            status=res["status"],
            is_terminal_state=res["isTerminalState"]
            if "isTerminalState" in res
            else None,
            remote_status=res["remoteStatus"] if "remoteStatus" in res else None,
            job_data_schema=res["jobDataSchema"] if "jobDataSchema" in res else None,
            job_data=res["jobData"] if "jobData" in res else None,
            child_jobs=child_jobs,
            files=files,
        )

    def is_complete(self) -> bool:
        """
        deprecated method, kept to limit number of changes
        required for extension SDKs
        """
        return self.is_terminal_state

    def wait_for_terminal_state(
        self, client: StrangweorksGQLClient, wait: int, poll_timeout: int
    ) -> None:
        """
        waits for a job to reach a terminal state, and refreshes the job
        """
        start_time = datetime.datetime.now()
        while not self.is_terminal_state:
            time.sleep(wait)
            job_response = get_job(client, self.workspace_slug, self.slug)
            self.status = (job_response["status"],)
            self.is_terminal_state = job_response["isTerminalState"]
            self.remote_status = job_response["remoteStatus"]
            if "files" in job_response:
                for _, f in job_response["files"]:
                    self.files.append(File.from_dict(f))
            if poll_timeout is not None and (
                (datetime.datetime.now().second - start_time.second) > poll_timeout
            ):
                raise StrangeworksError.timeout(
                    message=f"timeout attempting to fetch results after {poll_timeout}"
                )


get_job_request = Operation(
    query="""
        query getWorkspaceJobs($jobSlug: String!, $workspaceSlug: String!) {
            workspace(slug: $workspace_slug) {
                job(jobSlug: $job_slug) {
                    id
                    serviceIdentifier
                    slug
                    status
                    isTerminalState
                    remoteStatus
                    jobDataSchema
                    jobData
                    files
                }
            }
        }
        """
)


def get_job(
    client: StrangweorksGQLClient,
    workspace_slug: str,
    job_slug: str,
) -> Job:
    """Retrieve job info

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        identifier for the resource.
    id: str
        the job_slug identifier used to retrieve the job.

    Returns
    -------
    Job
        The ``Job`` object identified by the slug.
    """
    op = get_job_request
    platform_result = client.execute(
        op=op,
        **locals(),
    )
    return Job.from_dict(platform_result["job"])
