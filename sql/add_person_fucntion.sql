CREATE OR REPLACE FUNCTION add_person(
    p_name char(50),
    p_address char(50),
    p_email char(50),
    p_phone_number integer
)
    RETURNS VOID
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO person (name, address, email, phone_number)
    VALUES (p_name, p_address, p_email, p_phone_number);
END;
$$