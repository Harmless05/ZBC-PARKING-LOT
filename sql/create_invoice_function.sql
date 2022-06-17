CREATE OR REPLACE FUNCTION create_invoice
    (
        in_start_date date,
        in_end_date date,
        in_license_plate char(7),
        user_id integer
)
    RETURNS VOID
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO parking_history (parking_id, start_date, end_date, license_plate, user_id) Values (parking_id, in_start_date, in_end_date, in_license_plate, user_id);
END;
$$;