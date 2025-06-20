# Question:
# Design a Parking Lot Management System that:
# - Supports multiple vehicle types (car, bike, truck)
# - Allocates appropriate parking spots based on vehicle type
# - Issues parking tickets on entry
# - Calculates parking fees based on duration (minimum ₹10, ₹0.5/minute)
# - Handles payment at the time of exit
# - Unparks vehicles and frees up the spot after payment


from enum import Enum
import uuid
from datetime import datetime

class VehicleType(Enum):
    CAR = "car"
    BIKE = "bike"
    TRUCK = "truck"

class SpotType(Enum):
    COMPACT = "compact"
    LARGE = "LARGE"
    BIKE = "bike"


class Vehicle:
    def __init__(self, license_plate,vehicle_type:VehicleType) -> None:
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

class ParkingSpot:
    def __init__(self,spot_id,spot_type:SpotType) -> None:
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.vehicle = None
    
    def assign_vehicle(self,vehicle:Vehicle):
        self.vehicle = vehicle
        self.is_occupied = True
    
    def remove_vehicle(self):
        self.vehicle = None
        self.is_occupied = False

class Floor:
    def __init__(self,floor_number) -> None:
        self.floor_number = floor_number
        self.spots = []
    
    def add_spot(self,spot:ParkingSpot):
        self.spots.append(spot)
    
    def find_availability(self,vehicle_type:VehicleType):
        for spot in self.spots:
            if not spot.is_occupied:
                if ((vehicle_type == VehicleType.BIKE and spot.spot_type == SpotType.BIKE) or
                    (vehicle_type == VehicleType.CAR and spot.spot_type == SpotType.COMPACT) or 
                    (vehicle_type == VehicleType.TRUCK and spot.spot_type == SpotType.LARGE)):
                    return spot
        return None
    
    def __str__(self):
        return f"Floor {self.floor_number}"

class Ticket:
    def __init__(self,vehicle:Vehicle, spot : ParkingSpot, floor: Floor) -> None:
        self.ticket_id = (uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.floor = floor
        self.entry_time = datetime.now()

    def __str__(self) -> str:
        return f"TicketID : {self.ticket_id}, Vehicle : {self.vehicle.license_plate}, Floor : {str(self.floor)}, SpotID : {self.spot.spot_id}"
    
class Payment:
    def __init__(self, ticket: Ticket) -> None:
        self.ticket = ticket
        self.paid = False
        self.amount = self.calculate_amount()
        self.payment_time = None

    def calculate_amount(self):
        duration = (datetime.now() - self.ticket.entry_time).seconds // 60 
        rate_per_minute = 0.5  
        return max(10, duration * rate_per_minute)

    def make_payment(self):
        self.payment_time = datetime.now()
        self.paid = True
        print(f"Paid ₹{self.amount} for vehicle {self.ticket.vehicle.license_plate}")

class ParkingLot:
    def __init__(self) -> None:
        self.floors = []
    
    def add_floor(self,floor:Floor):
        self.floors.append(floor)

    def park_vehicle(self, vehicle: Vehicle):
        for floor in self.floors:
            spot = floor.find_availability(vehicle.vehicle_type)
            if spot:
                spot.assign_vehicle(vehicle)
                ticket = Ticket(vehicle,spot,floor)
                print(ticket)
                return ticket
        print("No available spot")
        return None

    def unpark_vehicle(self,ticket):
        payment = Payment(ticket)
        payment.make_payment()
        ticket.spot.remove_vehicle()
        print(f"Vehicle {ticket.vehicle.license_plate} unpark from floor {ticket.floor.floor_number}, spot {ticket.spot.spot_id}")

if __name__ == "__main__":
    lot = ParkingLot()

    #create floor
    floor1 = Floor(1)
    #add spot in the floor
    floor1.add_spot(ParkingSpot("A1",spot_type=SpotType.BIKE))
    floor1.add_spot(ParkingSpot("A2",spot_type=SpotType.COMPACT))

    #add floor to lot
    lot.add_floor(floor1)

    #create vehicle to add 
    Bike = Vehicle("Bike123", VehicleType.BIKE)

    #assign spot to vehicle 
    ticket1 = lot.park_vehicle(Bike)

    lot.unpark_vehicle(ticket1)
