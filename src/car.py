from database_manager import Base, Column, Integer, String, CheckConstraint, ForeignKey


class Car(Base):
    __tablename__ = "cars"
    #__table_args__ = (
    #    CheckConstraint("license_plate ~* '^([A-Za-z0-9]){1,7}$'", name="check_license_plate"),
    #)
    id = Column(Integer, primary_key=True)
    license_plate = Column(String)
    owner = Column(Integer, ForeignKey("users.id"))
