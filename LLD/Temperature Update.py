# Basic Observer Pattern with Temperature Update
# Design and implement a Weather Monitoring System that supports:
# A WeatherStation that can record temperature readings.
# One or more Thermostats (observers) that get notified whenever the temperature updates.
# Each thermostat simply logs or displays the most recent temperature when notified.

from abc import ABC, abstractmethod

#Observer
class Observer(ABC):
    @abstractmethod
    def display(self,temp:float):
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
    def display(self, temp: float):
        print(f"\n[ThermostatDisplay] Current temp : {temp}")

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
            observer.display(self._temperature)

# Test
if __name__ == "__main__":
    station = WeatherStation()

    t1 = Thermostat()
    t2 = Thermostat()

    station.add_observer(t1)
    station.add_observer(t2)

    station.set_temperature(25.5)
    station.set_temperature(30.2)