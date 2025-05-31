from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def drive(self):
        pass

class Car(Vehicle):
    def drive(self):
        print("Driving car.")

class Bike(Vehicle):
    def drive(self):
        print("Driving bike.")

class Truck(Vehicle):
    def drive(self):
        print("Driving truck.")

class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type: str) -> Vehicle:
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "bike":
            return Bike()
        elif vehicle_type == "truck":
            return Truck()
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
def user_driving(vehicle_type):
    try:
        vehicle = VehicleFactory.create_vehicle(vehicle_type)
        vehicle.drive()
    except ValueError as e:
        print(f"[ERROR] {e}")

sample_data = ["car","bike","truck","plane"]

for data in sample_data:
    user_driving(data)