import logging

# Setup simple logging configuration
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class PaymentMethod:
    def pay(self, amount: float):
        raise NotImplementedError("Subclass must implement pay method")

class CreditCard(PaymentMethod):
    def pay(self,amount):
        print(f"${amount} Payment Done using CreditCard")

class PayPal(PaymentMethod):
    def pay(self,amount):
        print(f"${amount} Payment Done using PayPal")

class Bitcoin(PaymentMethod):
    def pay(self,amount):
        print(f"${amount} Payment Done using Bitcoin")


class UnknownMethod(PaymentMethod):
    pass  # Forgot to implement pay()

# A function that uses polymorphism
def make_payment(pay_method: PaymentMethod, amount: float):
    try:
        pay_method.pay(amount)
    except NotImplementedError as e:
        error_msg = f"ERROR: {pay_method.__class__.__name__} does not implement 'pay': {e}"
        print(error_msg)
        logging.error(error_msg)  # Log the error message

pay_methods = [CreditCard(), PayPal(), Bitcoin(), UnknownMethod()]
payment_amounts = [100, 50.5, 200,75]

for method, amount in zip(pay_methods, payment_amounts):
    make_payment(method, amount)
