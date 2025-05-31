# Extend the Weather Monitoring System to support:
# - Thermostats should now keep track of the last 24 temperature readings.
# - Use a fixed-size structure (like deque) to store only the most recent 24 updates.
# - After each update, the Thermostat should display:
#   • The current temperature.
#   • The average temperature over the last 24 readings.


from abc import ABC, abstractmethod
from collections import deque

#Observer
class Observer(ABC):
    @abstractmethod
    def update(self,temp:float):
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

class Thermostat(Observer):
    def __init__(self) -> None:
        self.history = deque(maxlen=24)
    
    def update(self, temp: float):
        self.history.append(temp)
        self.display(temp)

    def display(self, temp: float):
        avg = sum(self.history) / len(self.history)
        print(f"[ThermostatDisplay] Current: {temp}°C | Last 24h Avg: {avg:.2f}°C")


# Concrete Subject
class WeatherStation(Subject):
    def __init__(self):
        self.observers = []
        self._temperature = None
    
    def set_temperature(self, temp: float):
        print(f"\n[WeatherStation] New temperature set: {temp}°C")
        self._temperature = temp
        self.notify_observer()

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observer(self):
        for observer in self.observers:
            observer.update(self._temperature)

# Test
if __name__ == "__main__":
    station = WeatherStation()

    t1 = Thermostat()
    t2 = Thermostat()

    station.add_observer(t1)
    station.add_observer(t2)

    station.set_temperature(25.5)
    station.set_temperature(30.2)