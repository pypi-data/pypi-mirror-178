"""RAW SQL templates"""
VIEW_WRAPPER = """
-- One would think they can use drop or replace
-- (but this does not allow you to alter the table schema between runs)
DROP VIEW IF EXISTS dune_user_generated.{{TableName}} CASCADE;
CREATE VIEW dune_user_generated.{{TableName}} AS (
{{Values}}
);
"""
