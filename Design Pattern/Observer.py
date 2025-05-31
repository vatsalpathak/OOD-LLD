from abc import ABC, abstractmethod


#Observer
class Observer(ABC):
    @abstractmethod
    def display(self,price:float):
        pass

#subject
class Subject(ABC):

    @abstractmethod
    def add_observer(self,observer: Observer):
        pass

    @abstractmethod
    def remove_observer(self,observer: Observer):
        pass

    def notify_observer(self):
        pass

#Concrete StockMarket
class StockMarket(Subject):

    def __init__(self) -> None:
        self._observers = []
        self._price = 0

    def change_price(self,new_price):
        self._price = new_price
        print(f"\n[StockMarket] Price updated to {new_price}")
        self.notify_observer()

    def add_observer(self, observer: Observer):
        self._observers.append(observer)
    
    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observer(self):
        for observer in self._observers:
            observer.display(self._price)

#Concrete observer
class PriceDisplay(Observer):
    def display(self, price: float):
        print(f"\n[PriceDisplay] Current price : {price}")

class PercentageChangeDisplay(Observer):
    
    def __init__(self) -> None:
        self.old_price = None
        self.percentage_change = 0

    def display(self, price: float):
        if self.old_price is None:
            print("\n[PercentageChangeDisplay] No previous data to compare.")
        else:
            self.percentage_change = (abs(price - self.old_price) * 100)//self.old_price
            if price > self.old_price:
                print(f"\n[PercentageChangeDisplay] Positive Percentage change of {self.percentage_change}%")
            else:
                print(f"\n[PercentageChangeDisplay] Negative Percentage change of {self.percentage_change}%")
        self.old_price = price

class ThresholdAlertDisplay(Observer):
    critical_price = 100
    def display(self, price: float):
        if price < 100:
            print(f"\n[ThresholdAlertDisplay] Price is below critical price {price}")
        else:
            print(f"\n[ThresholdAlertDisplay] Price is normal")

stock_market = StockMarket()

# Register observers
price_display = PriceDisplay()
percentage_display = PercentageChangeDisplay()
threshold_display = ThresholdAlertDisplay()

stock_market.add_observer(price_display)
stock_market.add_observer(percentage_display)
stock_market.add_observer(threshold_display)

# Simulate stock price updates
prices = [120, 140, 95, 80, 110]
for price in prices:
    stock_market.change_price(price)