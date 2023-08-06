    select
        my_bytes::bytea,
        my_number::numeric,
        my_string::text,
        my_date::timestamptz,
        my_boolean::bool
    from (VALUES
{{Values}}
    ) as _ (my_bytes, my_number, my_string, my_date, my_boolean)