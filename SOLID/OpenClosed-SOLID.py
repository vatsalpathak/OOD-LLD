from abc import ABC, abstractmethod
import math
class Shape(ABC):
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def calculate_area (self) -> float:
        pass
    def print_area(self,name):
        area = self.calculate_area()
        print(f"Area of {name} is {area:.2f}")

class Circle(Shape):
    def __init__(self,name,radius):
        super().__init__(name)
        self.radius = radius

    def calculate_area(self) -> float:
        return math.pi * self.radius**2

class Rectangle(Shape):
    def __init__(self,name,height,width):
        super().__init__(name)
        self.height = height
        self.width = width

    def calculate_area(self):
        return self.height*self.width
    
class Triangle(Shape):
    def __init__(self,name,height,base):
        super().__init__(name)
        self.height = height
        self.base = base

    def calculate_area(self):
        return 0.5 * self.height*self.base

shapes = [
    Circle("circle",5),
    Rectangle("rectangle",4,6),
    Triangle("triangle",6,4)
]

for shape in shapes:
    shape.print_area(shape.name)