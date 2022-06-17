from database_manager import Base, Column, Integer, String, CheckConstraint, ForeignKey


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = (
        CheckConstraint("card_number ~* '^[0-9]{16}$'", name="check_card_number"),
        CheckConstraint("cvv ~* '^[0-9]{3}$'", name="check_card_cvv"),
        CheckConstraint("exp_year ~* '^[0-9]{4}$'", name="check_card_exp_year"),
        CheckConstraint("exp_month ~* '^(1[0-2]|[1-9])$'", name="check_card_exp_month"),
    )
    card_number = Column(String, primary_key=True)
    cvv = Column(String)
    exp_year = Column(String)
    exp_month = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
