class Student:
    def __init__(self,name):
        self.__name = name
        self.__grade = 0
    
    def set_grade(self,grade):
        if 0<=grade<=100:
            self.__grade= grade
        else:
            raise ValueError('it must be between 0 and 100')
        
    def get_grade(self):
        print(f"\nGrade : {self.__grade}")
    
    def print_report(self):
        print(f"\nReport for {self.__name} is {self.__grade}")

student1 = Student("Alice")
student1.set_grade(75)
student1.get_grade()

student2 = Student("Bob")
try:
    student2.set_grade(120)
except Exception as e: 
    print(e)
student2.set_grade(85)
student2.get_grade()

student1.print_report()
student2.print_report()
print("\n")
