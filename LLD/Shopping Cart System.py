# Design and implement a Shopping Cart System that supports:
# Adding/removing products.
# Calculating the final payable amount


class Product:
    def __init__(self,id,name,price,category) -> None:
        self.product_id = id
        self.name = name 
        self.price = price
        self.category = category

class CartItem:
    def __init__(self,product,quantity = 1) -> None:
        self.product = product
        self.quantity = quantity

    def get_subtotal(self) -> float:
        return self.product.price * self.quantity
    
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
        if not self.items:
            print("Cart is empty.")
            return
        print("Shopping Cart Contents:")
        for item in self.items:
            print("  -", item)
        print(f"Total: ${self.get_total():.2f}")
    
if __name__ == "__main__":
    p1 = Product("p1", "Laptop", 1000.0, "Electronics")
    p2 = Product("p2", "Shoes", 100.0, "Fashion")

    cart = ShoppingCart()
    cart.add_item(p1, 2)
    cart.add_item(p2, 1)

    cart.print_cart()

    print("Cart total:", cart.get_total())


