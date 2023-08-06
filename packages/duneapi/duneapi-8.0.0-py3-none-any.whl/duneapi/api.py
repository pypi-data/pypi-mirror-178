"""
A simple framework for interacting with not officially supported DuneAnalytics API
Code adapted from https://github.com/itzmestar/duneanalytics
at commit bdccd5ba543a8f3679e2c81e18cee846af47bc52
"""
from __future__ import annotations

import json
import os
import time
from typing import Optional

from deprecated.classic import deprecated
from dotenv import load_dotenv
from requests import Session, Response

from .logger import set_log
from .query_template import VIEW_WRAPPER
from .response import (
    validate_and_parse_dict_response,
)
from .types import (
    DuneRecord,
    DuneQuery,
    Post,
    QueryParameter,
    execute_query_post_data,
    Network,
)
from .util import paginated_table_name, partition_array, drop_page_query

log = set_log(__name__)

BASE_URL = "https://dune.com"
GRAPH_URL = "https://core-hsr.dune.com/v1/graphql"
GET_URL = "https://app-api.dune.com/v1/graphql"


class FailedExecution(Exception):
    """Special Dune Error for failed query executions"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}"


class DuneAPI:
    """
    Acts as API client for dune.xyz. All requests to be made through this class.
    """

    def __init__(
        self,
        username: str,
        password: str,
        max_retries: int = 2,
        ping_frequency: int = 5,
    ):
        """
        Initialize the object
        :param username: username for dune.xyz
        :param password: password for dune.xyz
        """
        self.csrf = None
        self.auth_refresh = None
        self.token = None
        self.username = username
        self.password = password
        self.session = Session()
        self.max_retries = max_retries
        self.ping_frequency = ping_frequency
        headers = {
            "origin": BASE_URL,
            "sec-ch-ua": "empty",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "dnt": "1",
        }
        self.session.headers.update(headers)

    @staticmethod
    def new_from_environment() -> DuneAPI:
        """Initialize & authenticate a Dune client from the current environment"""
        load_dotenv()
        dune = DuneAPI(
            os.environ["DUNE_USER"],
            os.environ["DUNE_PASSWORD"],
        )
        # loging and fetch_auth token don't really need to be here
        dune.login()
        return dune

    def login(self) -> None:
        """Attempt to log in to dune.xyz & get the token"""
        login_url = BASE_URL + "/auth/login"
        csrf_url = BASE_URL + "/api/auth/csrf"
        auth_url = BASE_URL + "/api/auth"

        # fetch login page
        self.session.get(login_url)

        # get csrf token
        self.session.post(csrf_url)
        self.csrf = self.session.cookies.get("csrf")

        # try to log in
        form_data = {
            "action": "login",
            "username": self.username,
            "password": self.password,
            "csrf": self.csrf,
            "next": BASE_URL,
        }

        self.session.post(auth_url, data=form_data)
        self.auth_refresh = self.session.cookies.get("auth-refresh")

    def fetch_auth_token(self) -> None:
        """Fetch authorization token for the user"""
        session_url = BASE_URL + "/api/auth/session"

        response = self.session.post(session_url)
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            raise RuntimeError("Failed to fetch auth token", response.text)

    def refresh_auth_token(self) -> None:
        """Set authorization token for the user"""
        self.fetch_auth_token()
        self.session.headers.update({"authorization": f"Bearer {self.token}"})

    def initiate_query(self, query: DuneQuery) -> bool:
        """
        Initiates a new query.
        """
        post_data = query.upsert_query_post()
        response = self.post_dune_request(post_data)
        validate_and_parse_dict_response(response, post_data.key_map)
        # Return True to indicate method was success.
        return True

    @deprecated(
        version="3.1.0",
        reason="Execution only requires a query_id and parameters; use execute",
    )
    def execute_query(self, query: DuneQuery) -> str:
        """Executes query at query_id"""
        post_data = execute_query_post_data(query.query_id, query.parameters)
        response = self.post_dune_request(post_data)
        validate_and_parse_dict_response(response, post_data.key_map)
        return str(response.json()["data"]["execute_query_v2"]["job_id"])

    def execute(
        self, query_id: int, parameters: Optional[list[QueryParameter]] = None
    ) -> str:
        """Executes existing query at `query_id` with `parameters`"""
        if parameters is None:
            parameters = []
        post_data = execute_query_post_data(query_id, parameters)
        response = self.post_dune_request(post_data)
        validate_and_parse_dict_response(response, post_data.key_map)
        return str(response.json()["data"]["execute_query_v2"]["job_id"])

    def get_results(self, query: DuneQuery, job_id: str) -> list[DuneRecord]:
        """Fetch the result for a query by id"""
        get_execution_post = query.get_execution(job_id)
        execution_status = self.post_dune_request(get_execution_post, is_get=True)
        unnested_status = execution_status.json()["data"]["get_execution"]
        while unnested_status["execution_succeeded"] is None:
            failure_data = unnested_status["execution_failed"]
            if failure_data is not None:
                raise FailedExecution(
                    f"query {query.query_id} execution failed with {failure_data}"
                )
            queue_data = unnested_status["execution_queued"]
            if queue_data is not None:
                log.info(f"execution queued {queue_data}")
            running_data = unnested_status["execution_running"]
            if running_data is not None:
                log.info(f"execution running {running_data}")

            time.sleep(self.ping_frequency)
            execution_status = self.post_dune_request(get_execution_post, is_get=True)
            # TODO - make unnest method
            unnested_status = execution_status.json()["data"]["get_execution"]

        results: list[dict[str, str]] = unnested_status["execution_succeeded"]["data"]
        return results

    def post_dune_request(self, post: Post, is_get: bool = False) -> Response:
        """
        Refresh Authorization Token and posts query.
        Parses response for errors by key and raises runtime error if they exist.
        Only successful responses are returned
        :param post: JSON content and validation parameters for request
        :param is_get: random different url used when posting get_execution
        :return: response in json format
        """
        self.refresh_auth_token()
        log.debug(f"Posting Dune Request {json.dumps(post.data)}")
        post_url = GET_URL if is_get else GRAPH_URL
        response = self.session.post(post_url, json=post.data)
        log.debug(f"Received Response {response.json()}")

        return response

    def execute_and_await_results(self, query: DuneQuery) -> list[DuneRecord]:
        """
        Executes query by ID and awaits completion.
        :return: parsed list of dict records returned from query
        """
        job_id = self.execute(query.query_id, query.parameters)
        data_set = self.get_results(query, job_id)
        log.info(f"got {len(data_set)} records from last query")
        return data_set

    def fetch(self, query: DuneQuery) -> list[DuneRecord]:
        """
        Pushes new query, executes and awaiting query completion
        :return: list query records as dictionaries
        """
        log.info(f"Fetching {query.name} on {query.network}...")
        self.initiate_query(query)
        for _ in range(0, self.max_retries):
            try:
                return self.execute_and_await_results(query)
            except RuntimeError as err:
                log.warning(
                    f"failed with {err}. Re-establishing connection and trying again"
                )
                self.login()
                self.refresh_auth_token()
        raise Exception(f"Maximum retries ({self.max_retries}) exceeded")

    def upsert(self, query: DuneQuery) -> None:
        """Updates and executes `query`"""
        self.initiate_query(query)
        job_id = self.execute_query(query)
        # Get results is just a form of confirming that the upsert was executed
        _ = self.get_results(query, job_id)
        log.info(
            f"{query.name} successfully updated: https://dune.xyz/queries/{query.query_id}"
        )

    def _push_single_view(  # pylint: disable=too-many-arguments
        self,
        select_template: str,
        table_name: str,
        values: list[str],
        query_params: list[QueryParameter],
        separator: str = ",\n",
    ) -> None:
        """Pushes a user generated view to Dune Analytics via Legacy API"""
        raw_sql = select_template.replace("{{TableName}}", table_name).replace(
            "{{Values}}", separator.join(values)
        )
        data_size = len(raw_sql.encode("utf-8"))
        if data_size > 10**6:
            raise RuntimeError(
                f"Cannot push {data_size}Mb > 1Mb to Dune. Use multi_push_view!"
            )

        log.info(f"Pushing ~{len(raw_sql.encode('utf-8')) / 10 ** 6:.2f} Mb to Dune.")
        query = DuneQuery.from_environment(
            raw_sql=raw_sql,
            name=table_name,
            parameters=query_params,
            # TODO - allow other networks!
            network=Network.MAINNET,
        )
        self.upsert(query)

    def _multi_push_view(  # pylint: disable=too-many-arguments
        self,
        select_template: str,
        table_name: str,
        partitioned_values: list[list[str]],
        skip: int = 0,
    ) -> None:
        """
        Pushes the values from a partitioned list to multiple pages of tables,
        then builds a table out of the union of those pages
        """
        log.info(f"Creating {len(partitioned_values)} pages from partitioned list")
        aggregate_tables = []
        for page, chunk in enumerate(partitioned_values):
            page_name = paginated_table_name(table_name, page)

            if page >= skip:
                log.info(f"Pushing Page {page} to {page_name}")
                self._push_single_view(
                    select_template=VIEW_WRAPPER.replace("{{Values}}", select_template),
                    table_name=page_name,
                    values=chunk,
                    query_params=[
                        QueryParameter.text_type("TableName", page_name),
                    ],
                )
            else:
                log.info(f"skipping page {page}")
            aggregate_tables.append(
                f"select {page} as page, * from dune_user_generated.{page_name}"
            )
        # TODO - assert sorted values,
        #  - check if updates are even needed (by making a hash select statement)
        #  - Don't update pages that are unchanged

        # This combines all the pages into a single table.
        self._push_single_view(
            select_template=VIEW_WRAPPER,
            table_name=table_name,
            values=aggregate_tables,
            query_params=[],
            # Union All Preserves order!
            separator="\nunion all\n",
        )

    def push_view(
        self,
        table_name: str,
        select_template: str,
        values: list[str],
    ) -> None:
        """
        Public interface to push a dune user generated view.
        Checks the size of data being pushed and partition it into pages if necessary
        """
        data_size_mb = len("\n".join(values).encode("utf-8")) / 10**6
        if data_size_mb > 0.9:
            num_chunks = int(data_size_mb / 0.9) + 1  # this is always >= 2
            chunk_size = len(values) // num_chunks
            self._multi_push_view(
                select_template,
                table_name=table_name,
                partitioned_values=partition_array(values, chunk_size),
            )
        else:
            # TODO - allow QueryParameter forwarding (like environment)
            select_template = VIEW_WRAPPER.replace("{{Values}}", select_template)
            self._push_single_view(select_template, table_name, values, [])

    def _drop_page_set(self, table_name: str, pages: set[int]) -> None:
        """Dune SQL query to drop a range of order reward pages from `page_from` to `page_to`"""
        self.fetch(
            DuneQuery.from_environment(
                raw_sql="\n".join(
                    [drop_page_query(table_name, page) for page in pages]
                ),
                network=Network.MAINNET,
                name=f"Drop {table_name} pages {sorted(list(pages))}",
            )
        )

    def drop_view(self, table_name: str) -> None:
        """
        Drops all User generated views related to order rewards for `env`
        This includes all pages and any aggregate views that depend on them.
        """

        log.info(f"Dropping view {table_name} and all existing pages.")
        all_pages_query = f"""
        select distinct(replace(table_name, '{table_name}_page_', '')) as page
        from INFORMATION_SCHEMA.views
        where table_schema = 'dune_user_generated'
          and table_name ilike '{table_name}_page%';
        """
        all_pages = [
            int(row["page"])
            for row in self.fetch(
                DuneQuery.from_environment(
                    raw_sql=all_pages_query,
                    network=Network.MAINNET,
                    name=f"{table_name} distinct pages",
                )
            )
        ]
        self._drop_page_set(table_name, set(all_pages))
