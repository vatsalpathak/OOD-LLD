# Question:
# Design a Pizza Ordering System that:
# - Allows creating pizzas with various sizes and multiple toppings
# - Calculates price per pizza based on size and toppings
# - Supports adding multiple pizzas to an order
# - Provides a detailed order summary with individual pizza details and total cost
# - Processes payment and confirms successful transaction


class Pizza:
    BASE_PRICES = {
        'small': 200,
        'medium': 300,
        'large': 400
    }

    TOPPING_PRICES = {
        'cheese': 50,
        'mushrooms': 40,
        'pepperoni': 60,
        'olives': 30
    }

    def __init__(self,size):
        self.size = size
        self.toppings = []
    
    def add_topping(self,topping_name):
        self.toppings.append(topping_name)

    def calculate_price(self):
        base_price = self.BASE_PRICES[self.size]
        topping_price = 0
        for topping in self.toppings:
            topping_price += self.TOPPING_PRICES[topping]
        return ( base_price + topping_price)
    
    def summary(self):
        return {
            'size': self.size,
            'toppings': self.toppings,
            'price': self.calculate_price()
        }

class PizzaOrder:
    def __init__(self) -> None:
        self.pizzas = []

    def add_pizza(self,pizza: Pizza):
        self.pizzas.append(pizza)

    def get_order_summary(self):
        summary = []
        total = 0
        for i, pizza in enumerate(self.pizzas,1):
            info = pizza.summary()
            summary.append((i,info))
            total += info['price']
        return summary,total
    
class Payment:
    def __init__(self,order:PizzaOrder):
        self.order = order
        self.paid = False
        self.total = 0

    def make_payment(self):
        summary, total = self.order.get_order_summary()
        self.total = total
        print("\n ------ Bill -----")
        for i,pizza_info in summary:
            print(f"Pizza {i}: Size={pizza_info['size']}, Toppings  : {', '.join(pizza_info['toppings'])}, Price = {pizza_info['price']}")
        print(f"------------------------")
        print(f"Total Amount: ₹{self.total}")
        self.paid = True
        print("Payment Successful ✅")

if __name__ == "__main__":
    # Build pizzas
    pizza1 = Pizza('medium')
    pizza1.add_topping('cheese')
    pizza1.add_topping('olives')

    pizza2 = Pizza('large')
    pizza2.add_topping('pepperoni')
    pizza2.add_topping('mushrooms')

    # Build order
    order = PizzaOrder()
    order.add_pizza(pizza1)
    order.add_pizza(pizza2)

    # Make payment
    payment = Payment(order)
    payment.make_payment()
