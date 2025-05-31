from abc import ABC, abstractmethod

# Base class that supports the Liskov Substitution Principle
class PayableEmployee(ABC):
    def __init__(self,name:str,emp_type):
        self.name = name
        self.employee_type = emp_type

    @abstractmethod
    def get_payement(self) -> float:
        pass

    def print_payment(self):
        salary = self.get_payement()
        print(f"{self.name} who is {self.employee_type} is paid ${salary:.2f} this month")


# Full-time employee implementation
class FullTimeEmployee(PayableEmployee):
    def __init__(self,name,salary):
        super().__init__(name,self.__class__.__name__)
        self.salary = salary
    
    def get_payement(self) -> float:
        return self.salary

# Intern implementation    
class Intern(PayableEmployee):
    def __init__(self,name,stipend):
        super().__init__(name,self.__class__.__name__)
        self.stipend = stipend

    def get_payement(self) -> float:
        return self.stipend
    
# Contractor is NOT a PayableEmployee — doesn't participate in payment logic
class Contractor:
    def __init__(self,name,agnecy):
        self.name = name
        self.agency = agnecy
        self.employement_type = "Contract"

    def report(self):
        print(f"{self.name} who is a {self.employement_type} and managed by {self.agency}, not paid here")

employees = [
    FullTimeEmployee("John",2000),
    FullTimeEmployee("Jane",5000),
    Intern("Bob",1000)
]

for employee in employees:
    employee.print_payment()
    
contract = Contractor("Marry","xyz")
contract.report()
