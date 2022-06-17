CREATE OR REPLACE FUNCTION delete_card(
    c_card_number char(16),
    c_user_id integer
)
    RETURNS VOID
    LANGUAGE plpgsql
AS
$$
BEGIN
    DELETE FROM card WHERE card.card_number = c_card_number and card.user_id = c_user_id;
END;
$$