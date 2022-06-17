from database_manager import Base, Column, Integer, String, CheckConstraint


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("name ~* '^[A-Za-z]+$'", name="check_name"),
        CheckConstraint("email ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'", name="check_email"),
        CheckConstraint("phone_number ~* '^[0-9]{8}$'", name="check_phone_number"),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    administrator = Column(Integer, default=0)

    def __repr__(self):
        return "[User] ID: {} | Name: {} | Address: {} | Email: {} | Phone Number: {}"\
            .format(self.id, self.name, self.address, self.email, self.phone_number)
