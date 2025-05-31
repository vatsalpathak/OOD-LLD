# Design and implement a Shopping Cart System that supports:
# Adding/removing products.
# Applying a single discount to each cart item (the discount may differ per item, e.g., 10 off one, 5% off another).
# Calculating the final payable amount after applying item-level discounts.

from abc import ABC, abstractmethod

class Product:
    def __init__(self,id,name,price,category) -> None:
        self.product_id = id
        self.name = name 
        self.price = price
        self.category = category

class Discount(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass

class PercentageDiscount(Discount):
    def __init__(self, percentage: float) -> None:
        self.percentage = percentage
    
    def apply(self, amount: float) -> float:
        return amount * (1 - self.percentage / 100)

class FixedAmountDiscount(Discount):
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def apply(self, amount: float) -> float:
        return max(0, amount - self.amount)

class CartItem:
    def __init__(self,product,quantity = 1) -> None:
        self.product = product
        self.quantity = quantity

    def add_discount(self, discount: Discount):
        self.discount = discount

    def get_subtotal(self) -> float:
        subtotal = self.product.price * self.quantity
        if self.discount:
            return self.discount.apply(subtotal)
        return subtotal
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity} = ${self.get_subtotal():.2f}"

class ShoppingCart:
    def __init__(self) -> None:
        self.items = []

    def add_item(self,product,quantity):
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                return
        item = CartItem(product,quantity)
        self.items.append(item)

    def remove_item(self,product_id,quantity):
        for item in self.items:
            if item.product.product_id == product_id:
                if quantity is None or quantity >= item.quantity:
                    self.items.remove(item)
                else:
                    item.quantity -= quantity
                return
    
    def get_total(self):
        total = 0
        for item in self.items:
            total += item.get_subtotal()
        return total
    
    def print_cart(self):
        print("Cart Contents:")
        for item in self.items:
            line = f"{item.product.name} x{item.quantity} @ {item.product.price:.2f} each"
            if item.discount:
                line += f" -> Discounted: {item.get_subtotal():.2f}"
            else:
                line += f" -> Subtotal: {item.get_subtotal():.2f}"
            print(line)
    
if __name__ == "__main__":
    # Products
    p1 = Product("p1", "Laptop", 1200.0, "Electronics")
    p2 = Product("p2", "Shoes", 150.0, "Fashion")
    p3 = Product("p3", "Headphones", 200.0, "Electronics")
    p4 = Product("p4", "Book", 50.0, "Education")
    p5 = Product("p5", "Backpack", 80.0, "Accessories")

    # Create cart and add items
    cart = ShoppingCart()
    cart.add_item(p1, 1)  # 1200
    cart.add_item(p2, 2)  # 300
    cart.add_item(p3, 1)  # 200
    cart.add_item(p4, 3)  # 150
    cart.add_item(p5, 2)  # 160

    # Apply discounts
    cart.items[0].add_discount(FixedAmountDiscount(200))     # Laptop: -$200
    cart.items[1].add_discount(PercentageDiscount(10))       # Shoes: -10%
    cart.items[2].add_discount(FixedAmountDiscount(50))      # Headphones: -$50
    cart.items[3].add_discount(PercentageDiscount(20))       # Book: -20%
    cart.items[4].add_discount(FixedAmountDiscount(10))      # Backpack: -$10 per total

    # Output
    cart.print_cart()
    print("\nCart total after all discounts:", cart.get_total())
