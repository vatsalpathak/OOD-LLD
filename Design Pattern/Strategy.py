from abc import ABC, abstractmethod

# Step 1: Strategy Interface
class PayStrategy(ABC):
    @abstractmethod
    def pay(self,amount: float):
        pass

class CreditCard(PayStrategy):
    def pay(self,amount):
        print(f"\nPaying ${amount} using Credit Card")

class PayPal(PayStrategy):
    def pay(self,amount):
        print(f"\nPaying ${amount} using PayPal")

class Bitcoin(PayStrategy):
    def pay(self,amount):
        print(f"\nPaying ${amount} using Bitcoin")

class PaymentContext:
    def __init__(self, strategy: PayStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PayStrategy):
        self._strategy = strategy

    def make_payment(self, amount):
        self._strategy.pay(amount)

payer = PaymentContext(CreditCard())

payer.make_payment(20)

payer.set_strategy(PayPal())
payer.make_payment(60)

payer.set_strategy(Bitcoin())
payer.make_payment(75)
