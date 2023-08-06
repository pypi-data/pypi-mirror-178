import unittest

from duneapi.api import DuneAPI, VIEW_WRAPPER, FailedExecution
from duneapi.types import Network, QueryParameter, DuneQuery
from duneapi.util import open_query, partition_array


class TestDuneAnalytics(unittest.TestCase):
    def setUp(self) -> None:
        self.five = 5
        self.one = 1
        self.parameter_name = "IntParameter"
        self.column_name = "value"
        self.dune = DuneAPI.new_from_environment()
        self.mainnet_query = self.network_query(Network.MAINNET)

    def network_query(self, network: Network) -> DuneQuery:
        return DuneQuery.from_environment(
            # Note that consecutive double brace brackets in formatted strings
            # become single brace brackets, so this query is
            # select 5 - '{{IntParameter}}' as value
            raw_sql=f"select {self.five} - '{{{{{self.parameter_name}}}}}' as {self.column_name}",
            description="Test Description",
            network=network,
            parameters=[QueryParameter.number_type(self.parameter_name, self.one)],
            name="Test Fetch",
        )

    def test_initiate_query(self):
        self.assertEqual(True, self.dune.initiate_query(self.mainnet_query))

    def test_execute_query(self):
        q_id = self.mainnet_query.query_id
        params = self.mainnet_query.parameters
        self.assertNotEqual(None, self.dune.execute(q_id, params))

    def test_interface(self):
        """
        This test indirectly touches all of
        - fetch
        - initiate_new_query
        - execute_and_await_results
        - execute_query
        - post_dune_request
        - Tests that the API works on all supported "Networks"
        essentially all the methods of the API
        """
        dune = DuneAPI.new_from_environment()
        for network in Network:
            query = self.network_query(network)
            res = dune.fetch(query)
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0][self.column_name], self.five - self.one)

    def test_push_view_small(self):
        # This test passes through the un-partitioned route
        dune = DuneAPI.new_from_environment()
        values = [
            "('\\x12', 999999999999999, 'string1', '2022-12-25 12:34', True)",
            "('\\x34', 3.14159, 'string2', '2010-12-25 12:34', False)",
            "('\\x12', 9999999999999999, 'string1', '2022-12-25 12:34', True)",
            "('\\x12', '9999999999999999', 'string1', '2022-12-25 12:34', True)",
        ]
        # TODO - use dune_representation cast of actual value tuples.
        table_name = "killer_test_table"
        select_template = open_query("./tests/queries/sample_values_query.sql")

        dune.push_view(table_name, select_template, values)
        results = dune.fetch(
            DuneQuery.from_environment(
                f"select count(*) as num_rows from dune_user_generated.{table_name}",
                network=Network.MAINNET,
            )
        )
        self.assertEqual(results[0]["num_rows"], len(values))

    @unittest.skip(
        "This is too large, "
        "we can test this with a smaller example by calling the "
        "private method directly. See test_push_view_paginated_tiny"
    )
    def test_push_view_paginated(self):
        # This test passes through the un-partitioned route
        dune = DuneAPI.new_from_environment()
        values = [
            "('\\x123456789101112131415161', 999999999999999, 'string1', '2022-12-25 12:34', True)",
            "('\\x123456789101112131415161', 3.141595653569, 'string2', '2010-12-25 12:34', False)",
            "('\\x123456789101112131415161', 999999999999911, 'string1', '2022-12-25 12:34', True)",
            "('\\x123456789101112131415161', '9999999999999', 'string1', '2022-12-25 12:34', True)",
        ] * 10000

        self.assertEqual(len(values), 40000)
        data_size_mb = len("\n".join(values).encode("utf-8")) / 10**6
        self.assertGreater(data_size_mb, 0.9)
        # TODO - use dune_representation cast of actual value tuples.
        table_name = "killer_test_table"
        select_template = open_query("./tests/queries/sample_values_query.sql")

        dune.push_view(table_name, select_template, values)
        results = dune.fetch(
            DuneQuery.from_environment(
                f"select count(*) as num_rows from dune_user_generated.{table_name}",
                network=Network.MAINNET,
            )
        )
        self.assertEqual(results[0]["num_rows"], len(values))

    def test_push_view_paginated_tiny(self):
        # This test passes through the un-partitioned route
        dune = DuneAPI.new_from_environment()
        select_template = "select * from (VALUES {{Values}}) as _ (my_column)"
        values = [
            "('Pizza')",
            "('is')",
            "('amazing')",
        ]

        table_name = "killer_tiny_paginated_test_table"
        page_size = 2
        dune._multi_push_view(
            select_template,
            table_name=table_name,
            partitioned_values=partition_array(values, page_size),
        )
        num_pages = dune.fetch(
            DuneQuery.from_environment(
                f"select count(distinct page) as num_pages from dune_user_generated.{table_name}",
                network=Network.MAINNET,
            )
        )[0]["num_pages"]
        self.assertEqual(num_pages, len(values) // page_size + 1)
        first_results = dune.fetch(
            DuneQuery.from_environment(
                f"select * from dune_user_generated.{table_name}",
                network=Network.MAINNET,
            )
        )
        self.assertEqual(
            [
                {"my_column": "Pizza", "page": 0},
                {"my_column": "is", "page": 0},
                {"my_column": "amazing", "page": 1},
            ],
            first_results,
        )

        # Now to test overwrite:
        totally_new_select_statement = (
            "select * from (VALUES {{Values}}) as _ (my_column)"
        )
        totally_new_values = ["('Hello')", "('World!')"]
        dune._multi_push_view(
            select_template=totally_new_select_statement,
            table_name=table_name,
            partitioned_values=partition_array(totally_new_values, part_size=1),
        )
        second_results = dune.fetch(
            DuneQuery.from_environment(
                f"select * from dune_user_generated.{table_name}",
                network=Network.MAINNET,
            )
        )
        self.assertEqual(
            [
                {"my_column": "Hello", "page": 0},
                {"my_column": "World!", "page": 1},
            ],
            second_results,
        )

    def test_drop_view(self):
        # This test passes through the un-partitioned route
        dune = DuneAPI.new_from_environment()
        select_template = "select * from (VALUES {{Values}}) as _ (my_column)"
        values = list(map(lambda t: f"({t})", range(3)))
        table_name = "integer_table"
        dune._multi_push_view(
            select_template, table_name, partition_array(values, part_size=1)
        )
        view_query = DuneQuery.from_environment(
            raw_sql=f"select * from dune_user_generated.{table_name}",
            network=Network.MAINNET,
        )

        self.assertEqual(len(dune.fetch(view_query)), len(values))
        dune.drop_view(table_name)
        with self.assertRaises(FailedExecution):
            dune.fetch(view_query)


if __name__ == "__main__":
    unittest.main()
