import unittest
from datetime import datetime

from duneapi.util import (
    datetime_parser,
    open_query,
    duplicates,
    DUNE_DATE_FORMAT,
    partition_array,
    paginated_table_name,
)


class TestUtilities(unittest.TestCase):
    def test_date_parser(self):
        no_dates = {"a": 1, "b": "hello", "c": [None, 3.14]}
        self.assertEqual(datetime_parser(no_dates), no_dates)

        valid_date_str = "1985-03-10 05:00:00"
        invalid_date_str = "1985/03/10 - literally anything else"
        with_date = {"valid_date": valid_date_str, "invalid_date": invalid_date_str}
        self.assertEqual(
            datetime_parser(with_date),
            {
                "valid_date": datetime.strptime(valid_date_str, DUNE_DATE_FORMAT),
                "invalid_date": invalid_date_str,
            },
        )

    def test_open_query(self):
        query = "select 10 - '{{IntParameter}}' as value"
        self.assertEqual(query, open_query("./tests/queries/test_query.sql"))

    def test_duplicates(self):
        self.assertEqual(duplicates([1, 2]), [])
        self.assertEqual(duplicates([1, 2, 2, 4]), [2])
        self.assertEqual(duplicates([1, 1, 2, 2]), [1, 2])

        with self.assertRaises(TypeError) as err:
            duplicates([{"x": 1, "y": 2}])

    def test_partition_array(self):
        arr = [1, 2, 3]
        self.assertEqual(partition_array(arr, 3), [arr])
        self.assertEqual(partition_array(arr, 4), [arr])
        self.assertEqual(partition_array(arr, 2), [[1, 2], [3]])
        self.assertEqual(partition_array(arr, 1), [[1], [2], [3]])
        with self.assertRaises(ValueError):
            partition_array(arr, 0)

        self.assertEqual(
            [["('Hello')"], ["('World!')"]],
            partition_array(["('Hello')", "('World!')"], part_size=1),
        )
        arr = [
            "('Pizza')",
            "('is')",
            "('amazing')",
        ]
        self.assertEqual(
            [["('Pizza')", "('is')"], ["('amazing')"]], partition_array(arr, 2)
        )

    def test_paginated_table_name(self):
        table_name = "table_name"
        for i in range(10):
            self.assertEqual(
                paginated_table_name(table_name, i), "_page_".join([table_name, str(i)])
            )


if __name__ == "__main__":
    unittest.main()
