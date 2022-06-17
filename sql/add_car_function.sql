CREATE OR REPLACE FUNCTION add_car(
    c_license_plate char(7),
    user_id integer
)
    RETURNS VOID
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO car (license_id, license_plate, user_id) Values (license_id, c_license_plate, user_id);
END;
$$;