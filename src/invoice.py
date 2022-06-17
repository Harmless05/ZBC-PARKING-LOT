from sqlalchemy import DateTime
from database_manager import Base, Column, Integer, String, ForeignKey


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    license_plate = Column(String)
    parking_price = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
