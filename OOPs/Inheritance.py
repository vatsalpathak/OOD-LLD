class Vehicle:
    def __init__(self,name):
        self.name = name
    def start_engine(self):
        print(f"{self.name} engine started")

class Car(Vehicle):
    def __init__(self, name):
        super().__init__(name)
    def start_engine(self):
        super().start_engine()

class MoterCycle(Vehicle):
    def __init__(self, name):
        super().__init__(name)
    def start_engine(self):
        super().start_engine()

#car
car = Car("Car")
car.start_engine()

#car
moter_cycle = MoterCycle("MoterCycle")
moter_cycle.start_engine()
