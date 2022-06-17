CREATE OR REPLACE FUNCTION delete_car(
    f_license_plate char(7)
)
    RETURNS VOID
    LANGUAGE plpgsql
AS
$$
BEGIN
    DELETE FROM car WHERE car.license_plate = f_license_plate;
END;
$$