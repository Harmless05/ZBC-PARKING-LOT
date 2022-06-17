CREATE OR REPLACE FUNCTION get_invoice(
    in_user_id integer
)
    RETURNS TABLE
            (
                parking_id integer,
                start_date date,
                end_date date,
                license_plate char(7),
                user_id integer
            )
    LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
        SELECT * FROM parking_history WHERE user_id = in_user_id;
END;
$$;