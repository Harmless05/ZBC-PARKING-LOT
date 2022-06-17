CREATE OR REPLACE FUNCTION get_person(
    f_phone_number INTEGER
)
    RETURNS TABLE
            (
                person_name          CHAR(50),
                person_address       CHAR(50),
                person_email         CHAR(50),
                person_phone_number  INTEGER,
                person_administrator INTEGER
            )
    LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
        SELECT * FROM person WHERE person.phone_number = f_phone_number;
END;
$$;