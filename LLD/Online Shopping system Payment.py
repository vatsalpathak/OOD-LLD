# Extend the Online Shopping System to support basic simulated payments.
# Enhance the system to:
# - Support selection of payment methods during checkout.
# - Define different payment types: Credit Card, PayPal, Cash on Delivery.
# - Allow users to choose a payment method at the time of placing an order.
# - Store and display the selected payment method in the order details.
# - Ensure invalid or missing payment methods are handled gracefully.
# Note: This is only a simulation — actual payment processing is NOT required.
# Build on top of the existing system from Step 1.


from enum import Enum

class OrderStatus(Enum):
    CREATED = "Created"
    PLACED = "Placed"

class PaymentMethod(Enum):
    CREDIT_CARD = "Credit Card"
    PAYPAL = "PayPal"
    COD = "Cash on Delivery"


class User:
    def __init__(self,name,email,address) -> None:
        self.name = name 
        self.email = email
        self.address = address
        self.cart = ShoppingCart()
        self.orders = []

class Product:
    def __init__(self,id,name,price,stock) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

class ShoppingCart:
    def __init__(self) -> None:
        self.items = {}

    def add_item(self, product, quantity):
        # Check if the quantity is valid and product is in stock
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        
        if product.stock < quantity:
            print(f"Not enough stock for {product.name}. Available: {product.stock}")
            return
        
        if product.id in self.items:
            product, current_quantity = self.items[product.id]
            self.items[product.id] = (product, current_quantity + quantity)
        else:
            self.items[product.id] = (product,quantity)
        print(f"Added to cart.")

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            print(f"[Cart] Removed product {product_id} from cart.")

    def update_quantity(self, product_id, quantity):
        if product_id not in self.items:
            print("Product not in cart.")
            return
        if product_id in self.items:
            product, _ = self.items[product_id]
            if quantity <= 0:
                del self.items[product_id]
            else:
                self.items[product_id] = (product,quantity)
            print(f"[Cart] Updated quantity of {product.name} to {quantity}.")

    def clear(self):
        # Empty the cart
        self.items.clear()
        print("[Cart] Cart cleared.")

    def get_subtotal(self):
        subtotal = 0
        for product, quantity in self.items.values():
            subtotal +=  product.price * quantity
        return subtotal
    
    def print_cart(self):
        print("\n Cart Contents:")
        if not self.items:
            print("  (Empty)")
        for product, qty in self.items.values():
            print(f"  {product.name} x {qty} = ${product.price * qty:.2f}")
        print(f"  Total: ${self.get_subtotal():.2f}")

class Order:
    def __init__(self,user,payment_method=None) -> None:
        self.user = user
        self.items = []
        self.order_status = OrderStatus.CREATED
        self.total_cost = 0
        self.payment_method = payment_method

    def add_items(self, cart_items):
        self.items.extend(cart_items)
        self.total_cost = sum(product.price * quantity for product, quantity in cart_items)
        self.order_status = OrderStatus.PLACED

    def print_order(self):
        print("\n Order Details:")
        for product, qty in self.items:
            print(f"  {product.name} x {qty} = ${product.price * qty:.2f}")
        print(f"  Status: {self.order_status.value}")
        print(f"  Payment Method: {self.payment_method.value}")
        print(f"  Total Cost: ${self.total_cost:.2f}")

class Amazon:
    def __init__(self) -> None:
        self.users = []
        self.products = []

    def add_user(self,name,email,address):
        user = User(name,email,address)
        self.users.append(user)
        print(f"Registered user: {name}")
        return user

    def add_product(self,id,name,price,stock):
        product = Product(id,name,price,stock)
        self.products.append(product)
        print(f"Added product: {name} - ${price:.2f} - Stock: {stock}")
        return product
    
    def checkout(self, user,payment_method):
        if not user.cart.items:
            print("Cart is empty. Cannot checkout.")
            return None
        
        if not isinstance(payment_method, PaymentMethod):
            print("Invalid payment method.")
            return None
        
        for product, quantity in user.cart.items.values():
            if product.stock < quantity:
                print(f"Insufficient stock for {product.name}")
                return None
            
        order = Order(user,payment_method)
        order.add_items(list(user.cart.items.values()))

        for product, qty in user.cart.items.values():
            product.stock -= qty

        user.orders.append(order)

        user.cart.clear()

        print(f"Order placed successfully! Total: ${order.total_cost:.2f} using {payment_method.value}!")
        return order

if __name__ == "__main__":
    # ------------------- RUNNING EXAMPLE --------------------
    amazon = Amazon()

    # Add Products
    laptop = amazon.add_product("p1", "Laptop", 1500.00, 2)
    phone = amazon.add_product("p2", "Phone", 800.00, 1)
    keyboard = amazon.add_product("p3", "Keyboard", 100.00, 5)

    # Add Users
    alice = amazon.add_user("Alice", "alice@mail.com", "NYC")
    bob = amazon.add_user("Bob", "bob@mail.com", "LA")
    carol = amazon.add_user("Carol", "carol@mail.com", "Chicago")

    # ---------- USER 1: Alice places valid order ----------
    alice.cart.add_item(laptop, 1)
    alice.cart.add_item(keyboard, 2)
    alice.cart.print_cart()
    amazon.checkout(alice, PaymentMethod.CREDIT_CARD)

    # ---------- USER 2: Bob tries to buy more than stock ----------
    bob.cart.add_item(phone, 2)  # Only 1 phone in stock
    bob.cart.print_cart()
    amazon.checkout(bob, PaymentMethod.PAYPAL)  # Should fail

    # ---------- USER 3: Carol tries to checkout with empty cart ----------
    carol.cart.print_cart()
    amazon.checkout(carol, PaymentMethod.COD)  # Should fail
