CREATE OR REPLACE FUNCTION get_car(
    f_license_plate char(7)
)
    RETURNS TABLE
            (
                car_license_id    INTEGER,
                car_license_plate CHAR(7),
                user_id           integer
            )
    LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
        SELECT * FROM car WHERE car.license_plate = f_license_plate;
END;
$$;