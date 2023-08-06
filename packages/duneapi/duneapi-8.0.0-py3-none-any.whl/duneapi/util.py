"""Utility methods to support Dune API"""
import collections
from datetime import datetime
from typing import Any, Hashable

DUNE_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def postgres_date(date_str: str) -> datetime:
    """Parse a postgres compatible date string into datetime object"""
    return datetime.strptime(date_str, DUNE_DATE_FORMAT)


def datetime_parser(dct: dict[str, Any]) -> dict[str, Any]:
    """
    Used as object hook in json loads method to parse postgres dates strings
    """
    for key, val in dct.items():
        if isinstance(val, str):
            try:
                dct[key] = datetime.strptime(val, DUNE_DATE_FORMAT)
            except ValueError:
                pass
    return dct


def open_query(filepath: str) -> str:
    """Opens `filename` and returns as string"""
    with open(filepath, "r", encoding="utf-8") as query_file:
        return query_file.read()


def duplicates(arr: list[Hashable]) -> list[Hashable]:
    """Detects and returns duplicates in array"""
    return [item for item, count in collections.Counter(arr).items() if count > 1]


def partition_array(arr: list[Any], part_size: int) -> list[list[Any]]:
    """Partitions array into parts of size `part_size`"""
    if part_size <= 0:
        raise ValueError(f"Can't partition array into parts of size {part_size}")
    return [arr[i : i + part_size] for i in range(0, len(arr), part_size)]


def paginated_table_name(table_name: str, page: int) -> str:
    """appends page number to a table name"""
    return f"{table_name}_page_{page}"


def drop_page_query(table_name: str, page: int) -> str:
    """Dune SQL query to drop table page"""
    # -- In order to drop a page, must drop any view or table which depending on it (i.e. cascade)
    schema = "dune_user_generated"
    return f"DROP VIEW IF EXISTS {schema}.{table_name}_page_{page} CASCADE;"
