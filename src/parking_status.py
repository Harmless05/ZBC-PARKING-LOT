import enum


class ParkingStatus(enum.Enum):
    Available = 1
    Reserved = 2
    Occupied = 3
    Unknown = 4
    
