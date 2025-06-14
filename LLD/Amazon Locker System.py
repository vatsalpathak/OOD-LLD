# GOAL:
# Implement a simplified Amazon Locker system for delivering and picking up eligible items.

# FEATURES:
# 1. Users can place an order with a locker-eligible item.
# 2. Lockers contain slots of different sizes.
# 3. Assign an available slot in a locker based on item size.
# 4. Generate a 6-digit access code upon assignment.
# 5. Users can pick up their item using the access code.
# 6. Automatically expire orders if not picked up in 3 days.

# ASSUMPTIONS / LIMITATIONS:
# - Lockers are always open (no store hours).
# - All lockers are assumed to be nearby (no geo logic).
# - Each order has only 1 item.
# - Return flow is not implemented yet.

from enum import Enum
from datetime import datetime, timedelta
from random import randint


class User:
    def __init__(self,email):
        self.email = email

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

    def assign(self,order):
        self.status = SlotStatus.OCCUPIED
        self.order = order
        self.delivery_time = datetime.now()
        self.access_code = self._generate_code()
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

class Locker:
    def __init__(self,locker_id) -> None:
        self.locker_id = locker_id
        self.slots = []

    def add_slot(self,slot):
        self.slots.append(slot)

    def find_available_slots(self,item_size):
        if self.slots:
            for slot in self.slots:
                if slot.size == item_size and slot.status == SlotStatus.AVAILABLE:
                    return slot
        return None
        
class LockerManager:
    def __init__(self) -> None:
        self.order = {}
        self.lockers = []

    def add_locker(self, locker):
        self.lockers.append(locker)

    def place_order(self,order):
        self.order[order.order_id] = order
    
    def assign_slot_to_order(self, order):
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
                return True
        
        print("No available slot found.")
        return False
    
    def pickup_order(self, order_id, access_code):
        order = self.order[order_id]
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


if __name__ == "__main__":
    print("=== Amazon Locker System Simulation Start ===\n")

    # Create a user
    print("Creating user...")
    user = User("alice@example.com")
    print(f"User created: {user.email}\n")

    # Create a locker-eligible item
    print("Creating item...")
    item = Item(name="Book", size="MEDIUM", is_locker_eligible=True)
    print(f"Item created: {item.name}, Size: {item.size}, Locker Eligible: {item.is_locker_eligible}\n")

    # Place an order
    print("Placing order...")
    order = Order(order_id="ORD123", user=user, item=item)
    print(f"Order placed: {order.order_id} for user {order.user.email} and item {item.name}\n")

    # Create locker and slots
    print("Creating locker and adding slots...")
    slot1 = Slot(slot_id="S1", size="MEDIUM")
    slot2 = Slot(slot_id="S2", size="LARGE")
    locker = Locker(locker_id="L1")
    locker.add_slot(slot1)
    locker.add_slot(slot2)
    print(f"Locker created: {locker.locker_id} with slots {[slot.slot_id for slot in locker.slots]}\n")

    # Initialize LockerManager
    print("Initializing locker manager...")
    manager = LockerManager()
    manager.add_locker(locker)
    print("Locker added to manager.\n")

    # Assign slot to order
    print("Processing order placement...")
    manager.place_order(order)
    print("Attempting to assign slot to order...")
    success = manager.assign_slot_to_order(order)

    if success:
        print(f"Access code sent to user: {order.access_code}\n")

        # Simulate pickup with correct code
        print("Simulating pickup with correct code...")
        correct_code = order.access_code
        manager.pickup_order(order.order_id, correct_code)
        print(f"Order status after pickup: {order.status.name}\n")

        # Attempt pickup again (should fail)
        print("Trying pickup again with same code (should fail)...")
        manager.pickup_order(order.order_id, correct_code)
        print()

    else:
        print("Could not assign locker.\n")

    # Create a new order that cannot be fulfilled
    print("Simulating new order that cannot be fulfilled...")
    new_item = Item(name="Guitar", size="XL", is_locker_eligible=True)
    new_order = Order(order_id="ORD124", user=user, item=new_item)
    manager.place_order(new_order)
    result = manager.assign_slot_to_order(new_order)
    if not result:
        print("No XL slot found for Guitar.\n")

    # Simulate expiration by backdating delivery time
    print("Simulating expiration of an order...")
    expired_order = Order(order_id="ORD125", user=user, item=item)
    manager.place_order(expired_order)
    manager.assign_slot_to_order(expired_order)

    # Backdate the delivery time to force expiration
    expired_order.slot.delivery_time -= timedelta(days=4)
    print(f"Manually updated delivery time to: {expired_order.slot.delivery_time}")
    print("Running expiration check...")
    manager.expire_orders()
    print(f"Order status after expiration check: {expired_order.status.name}\n")

    print("=== Simulation Complete ===")
