# Question:
# Design a Pizza Ordering system that:
# - Supports multiple pizza sizes with different base prices
# - Allows adding multiple toppings with individual prices
# - Calculates total price combining base price and toppings cost
# - Provides a summary of the order including size, toppings, and total price


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
        total = self.calculate_price()
        print(f"\nSize      : {self.size}")
        print(f"Toppings  : {', '.join(self.toppings)}")
        print(f"Total     : ₹{total}")



if __name__ == "__main__":
    pizza = Pizza(size='medium')
    pizza.add_topping('cheese')
    pizza.add_topping('olives')
    print(pizza.calculate_price() )
    pizza.summary()
