from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self,message):
        pass

class ConsoleLogger(Logger):
    def __init__(self):
        print("\nConsole logger Started")
    
    def log(self,message):
        print(f"\n console : \n\n{message}\n")

class FileLogger(Logger):
    def __init__(self):
        print("\nFile logger Started")
    
    def log(self,message):
        print(f"\n file : \n\n{message}\n")

class Log:
    def __init__(self,logger:Logger):
        self.logger = logger
    def log(self,message):
        self.logger.log(message)

#console
console = Log(ConsoleLogger())
console.log("Inside console logger")

#file
file = Log(FileLogger())
file.log("Inside file logger")