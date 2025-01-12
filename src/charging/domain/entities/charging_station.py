# src/charging/domain/entities/charging_station.py
class ChargingStation:
    def __init__(self, id, name, location, postal_code, status):
        self.id = id
        self.name = name
        self.location = location  # (lat, lon)
        self.postal_code = postal_code
        self.status = status  # e.g., "available", "occupied"
