CREATE OR REPLACE FUNCTION get_card(
    f_user_id integer
)
    RETURNS TABLE
            (
                card_card_number      char(16),
                card_cvv              integer,
                card_expiration_month integer,
                card_expiration_year  integer
            )
    LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
        SELECT * FROM card WHERE card.user_id = f_user_id;
END;
$$;