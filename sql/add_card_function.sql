CREATE OR REPLACE FUNCTION add_card(
    c_card_number char(16),
    c_cvv integer,
    c_expiration_month integer,
    c_expiration_year integer,
    c_user_id integer
)
    RETURNS VOID
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO card (card_number, cvv, expiration_month, expiration_year, user_id)
    VALUES (c_card_number, c_cvv, c_expiration_month, c_expiration_year, c_user_id);
END;
$$;