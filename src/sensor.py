from database_manager import Base, Column, Integer, ForeignKey, Enum, DateTime, Float
from parking_status import ParkingStatus


class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    parking_status = Column(Enum(ParkingStatus))
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    def serialize(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "parking_status": self.parking_status.value,
        }
