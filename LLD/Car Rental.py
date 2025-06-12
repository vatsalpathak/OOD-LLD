# Design a Car Rental System

# You are tasked with designing a system that allows users to rent cars. 
# The system should support user registration, adding vehicles, browsing available vehicles with filters, 
# and making or canceling reservations.

# Features to Implement
# Add vehicles with properties like type, make, license plate, price, and availability.

# Register users with unique IDs and driving license numbers.

# Search available vehicles using different filters (e.g., type, max price).

# Make reservations for specific date ranges.

# Cancel reservations and make vehicles available again.

from enum import Enum
from abc import ABC, abstractmethod
import uuid
from datetime import datetime
from typing import List

class VehicleType(Enum):
    SUV = "suv"
    SEDAN = "sedan"
    LUXURY = "luxury"

class Car:
    def __init__(self,type,make,license_plate,price) -> None:
        self.type = type
        self.make = make
        self.license_plate = license_plate
        self.price = price
        self.is_available = True

    def reserve(self):
        self.is_available = False

    def unreserve(self):
        self.is_available = True


class VehicleFilter(ABC):
    @abstractmethod
    def apply(self, car: Car) -> bool:
        pass

class TypeFilter(VehicleFilter):
    def __init__(self, vehicle_type: VehicleType):
        self.vehicle_type = vehicle_type

    def apply(self, car: Car) -> bool:
        return car.type == self.vehicle_type

class PriceFilter(VehicleFilter):
    def __init__(self, max_price: float):
        self.max_price = max_price

    def apply(self, car: Car) -> bool:
        return car.price <= self.max_price


class User:
    def __init__(self,driving_license) -> None:
        self.id = uuid.uuid4()
        self.driving_license = driving_license

class Reservation:
    def __init__(self,user,car,from_date,to_date) -> None:
        self.id = uuid.uuid4()
        self.user = user
        self.car = car
        self.from_date = from_date
        self.to_date = to_date
        self.status = "ACTIVE"

    def cancel(self):
        self.status = "CANCELLED"

class RentalSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self.vehicles = []
        self.users = []
        self.reservations = []
        self._initialized = True

    def register_user(self,driving_license):
        user = User(driving_license)
        self.users.append(user)

    def add_vehicle(self,car):
        self.vehicles.append(car)

    def search_vehicles(self,filters):
        result = []
        for car in self.vehicles:
            if not car.is_available:
                continue
            for f in filters:
                if f.apply(car):
                    result.append(car)
        return result
    
    def make_reservation(self,user,car,from_date,to_date):
        if not car.is_available:
            print("Car not available")
            return None
        
        reservation = Reservation(user,car,from_date,to_date)
        self.reservations.append(reservation)
        car.reserve()
        return reservation
    
    def cancel_reservation(self,reservation):
        reservation.cancel()
        reservation.car.unreserve()

if __name__ == "__main__":
    system = RentalSystem()

    #vehicles
    car1 = Car(VehicleType.SUV, "Toyota", "ABC123", 100)
    car2 = Car(VehicleType.SEDAN, "Honda", "XYZ456", 70)
    system.add_vehicle(car1)
    system.add_vehicle(car2)

    # Register user
    user = system.register_user("DL12345")

    # Search
    filters = [TypeFilter(VehicleType.SUV), PriceFilter(120)]
    available = system.search_vehicles(filters)
    print("Available Cars:")
    for car in available:
        print(car.make, car.license_plate, car.price)

    from datetime import timedelta
    from_date = datetime.now()
    to_date = from_date + timedelta(days=2)
    reservation = system.make_reservation(user,available[0],from_date,to_date)
    print("Reservation ID:", reservation.id)

    # Cancel reservation
    system.cancel_reservation(reservation)
    print("Reservation canceled. Status:", reservation.status)