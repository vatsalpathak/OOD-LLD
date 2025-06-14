# GOAL:
# Extend the basic locker system with real-world constraints and return logic.

# NEW FEATURES:
# 1. Assign the nearest locker based on user’s geo-location.
# 2. Locker access is restricted to store opening/closing hours.
# 3. Items that are not locker-eligible (e.g., furniture) cannot be delivered to lockers.
# 4. Support item returns via locker (if eligible).
# 5. Access code is invalid after locker is closed once.
# 6. Notify user with locker access code after delivery.

# NOTES:
# - Return flow is only supported for locker-eligible items.
# - Distance calculation may be mocked or simplified.
# - Opening/closing hours are assigned to lockers directly.
# - A scheduler or polling mechanism would be ideal for checking expirations.

from enum import Enum
from datetime import datetime, timedelta, time
from random import randint


class User:
    def __init__(self,email, location):
        self.email = email
        self.location = location

class Item:
    def __init__(self, name, size, is_locker_eligible) -> None:
        self.name = name 
        self.size = size
        self.is_locker_eligible = is_locker_eligible        

class OrderStatus(Enum):
    PLACED = "PLACED"
    DELIVERED = "DELIVERED"
    PICKED_UP = "PICKED_UP"
    EXPIRED = "EXPIRED"
    RETURN_PLACED = "RETURN_PLACED"   # New status for returns
    RETURNED = "RETURNED"             # Item successfully returned

class Order:
    def __init__(self,order_id,user,item) -> None:
        self.order_id = order_id
        self.user = user
        self.item = item
        self.status = OrderStatus.PLACED
        self.locker = None
        self.slot = None
        self.access_code = None
        self.delivery_time = None
        self.pickup_time = None  
        self.return_time = None        # For returns

class SlotStatus(Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    

class Slot:
    def __init__(self,slot_id,size) -> None:
        self.slot_id = slot_id
        self.size = size
        self.status = SlotStatus.AVAILABLE
        self.access_code = None
        self.order = None
        self.delivery_time = None
        self.code_valid = True          # New flag: access code validity

    def assign(self,order):
        self.status = SlotStatus.OCCUPIED
        self.order = order
        self.delivery_time = datetime.now()
        self.access_code = self._generate_code()
        self.code_valid = True
        return self.access_code
    
    def is_expired(self):
        if not self.delivery_time:
            return False
        return (datetime.now() - self.delivery_time).days >= 3
    
    def _generate_code(self):
        code = str(randint(1000,9999))
        return code
    
    def reset(self):
        self.status = SlotStatus.AVAILABLE
        self.delivery_time = None
        self.order = None
        self.access_code = None
        self.code_valid = True

class Locker:
    def __init__(self,locker_id, location,opening_time,closing_time) -> None:
        self.locker_id = locker_id
        self.locker_location = location
        self.slots = []
        self.opening_time = opening_time        # Added opening hour (datetime.time)
        self.closing_time = closing_time        # Added closing hour (datetime.time)
        self.last_closing_datetime = None       # Track last time locker closed

    def add_slot(self,slot):
        self.slots.append(slot)

    def find_available_slots(self,item_size):
        if self.slots:
            for slot in self.slots:
                if slot.size == item_size and slot.status == SlotStatus.AVAILABLE:
                    return slot
        return None
    
    def is_open_now(self):
        now_time = datetime.now().time()
        # Handles overnight hours as well if needed
        if self.opening_time <= self.closing_time:
            return self.opening_time <= now_time < self.closing_time
        else:
            # e.g., open 22:00 to 06:00 next day
            return now_time >= self.opening_time or now_time < self.closing_time

    def close_locker(self):
        self.last_closing_datetime = datetime.now()
        # When locker closes, invalidate all occupied slot access codes
        for slot in self.slots:
            if slot.status == SlotStatus.OCCUPIED:
                slot.code_valid = False
        
class LockerManager:
    def __init__(self) -> None:
        self.order = {}
        self.lockers = []

    def add_locker(self, locker):
        self.lockers.append(locker)

    def _calculate_distance(self, loc1, loc2):
        # Simplified mocked distance:
        # If locations are strings, return 0 if same, else 1
        return 0 if loc1 == loc2 else 1


    def place_order(self,order):
        self.order[order.order_id] = order
    
    def assign_slot_to_order(self, order):

        # Reject non-locker-eligible items immediately
        if not order.item.is_locker_eligible:
            print(f"Order {order.order_id} rejected: Item '{order.item.name}' not locker-eligible.")
            return False

        # Sort lockers by distance to user (nearest first)
        sorted_lockers = sorted(
            self.lockers,
            key=lambda l: self._calculate_distance(order.user.location, l.locker_location)
        )

        for locker in self.lockers:
            slot = locker.find_available_slots(order.item.size)

            if slot:
                code = slot.assign(order)
                order.status = OrderStatus.DELIVERED
                order.slot = slot
                order.locker = locker
                order.access_code = code
                order.delivery_time = slot.delivery_time
                print(f"Order {order.order_id} assigned to locker {locker.locker_id} with code {code}")
                # Notify user (simulate)
                print(f"Notification sent to {order.user.email}: Access code for locker {locker.locker_id} is {code}")
                return True
        
        print("No available slot found.")
        return False
    
    def pickup_order(self, order_id, access_code):
        order = self.order[order_id]
        #check for slot
        if not order or not order.slot:
            print(f"Order {order_id} not found or no slot assigned.")
            return False
        #check for locker close?
        locker = order.locker
        if not locker.is_open_now():
            print(f"Locker {locker.locker_id} is currently closed. Cannot pickup.")
            return False
        #pickup
        if order.slot.access_code == access_code:
            order.status = OrderStatus.PICKED_UP
            order.pickup_time = datetime.now()
            order.slot.reset()
            print("Pickup successful")
            return True
        print("Invalid access code.")
        return False
    
    def expire_orders(self):
        for order in self.order.values():
            if order.status == OrderStatus.DELIVERED and order.slot.is_expired():
                order.status = OrderStatus.EXPIRED
                order.slot.reset()
                print(f"Order {order.order_id} expired.")

    def return_order(self, order):
        # Only locker eligible items can be returned
        if not order.item.is_locker_eligible:
            print(f"Return rejected: Item '{order.item.name}' not eligible for locker return.")
            return False

        # Find nearest open locker with available slot
        sorted_lockers = sorted(
            self.lockers,
            key=lambda l: self._calculate_distance(order.user.location, l.locker_location)
        )

        for locker in sorted_lockers:
            if not locker.is_open_now():
                continue
            slot = locker.find_available_slots(order.item.size)
            if slot:
                code = slot.assign(order)
                order.status = OrderStatus.RETURN_PLACED
                order.slot = slot
                order.locker = locker
                order.access_code = code
                order.delivery_time = slot.delivery_time
                print(f"Return for order {order.order_id} assigned to locker {locker.locker_id} with code {code}")
                print(f"Notification sent to {order.user.email}: Return access code is {code}")
                return True

        print("No available slot found in any open locker for return.")
        return False

if __name__ == "__main__":
    print("=== Amazon Locker System Simulation Start ===\n")

    # Create a user
    user = User("alice@example.com", location='US')

    # Create locker-eligible and non-eligible items
    book = Item(name="Book", size="MEDIUM", is_locker_eligible=True)
    chair = Item(name="Chair", size="LARGE", is_locker_eligible=False)

    # Create lockers with opening/closing times (e.g., 9am to 9pm)
    locker1 = Locker(locker_id="L1", location='US', opening_time=time(9, 0), closing_time=time(21, 0))
    locker2 = Locker(locker_id="L2", location='CA', opening_time=time(10, 0), closing_time=time(20, 0))

    # Add slots to lockers
    locker1.add_slot(Slot(slot_id="S1", size="MEDIUM"))
    locker1.add_slot(Slot(slot_id="S2", size="LARGE"))
    locker2.add_slot(Slot(slot_id="S3", size="MEDIUM"))
    locker2.add_slot(Slot(slot_id="S4", size="LARGE"))

    manager = LockerManager()
    manager.add_locker(locker1)
    manager.add_locker(locker2)

    # Place and assign order for locker-eligible item
    order1 = Order(order_id="ORD001", user=user, item=book)
    manager.place_order(order1)
    print("\nAssigning locker for order1 (eligible item):")
    manager.assign_slot_to_order(order1)

    # Try to place order for non-eligible item
    order2 = Order(order_id="ORD002", user=user, item=chair)
    manager.place_order(order2)
    print("\nAssigning locker for order2 (non-eligible item):")
    manager.assign_slot_to_order(order2)

    # Simulate pickup with correct code during open hours
    print("\nAttempting pickup with correct code during open hours:")
    manager.pickup_order(order1.order_id, order1.access_code)

    # Simulate locker closing and access code invalidation
    print("\nSimulating locker closing and invalidation of access codes:")
    locker1.close_locker()

    # Trying pickup again after locker closed (should fail)
    print("\nAttempting pickup with same code after locker closed:")
    manager.pickup_order(order1.order_id, order1.access_code)

    # Place return order for locker-eligible item
    print("\nPlacing return order for locker-eligible item:")
    manager.return_order(order1)

    # Try to return non-eligible item
    print("\nTrying to return non-eligible item:")
    manager.return_order(order2)

    # Simulate expiration logic
    print("\nSimulating expiration:")
    expired_order = Order(order_id="ORD003", user=user, item=book)
    manager.place_order(expired_order)
    manager.assign_slot_to_order(expired_order)

    # Backdate delivery time to force expiration
    expired_order.slot.delivery_time -= timedelta(days=4)
    print(f"Backdated delivery time to: {expired_order.slot.delivery_time}")
    manager.expire_orders()

    print("\n=== Simulation Complete ===")