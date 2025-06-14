# Design a system for Alexa that supports custom user-defined commands like:

# “Start coffee machine”
# “Turn off all lights”

# Each command:
#    Should be encapsulated as a Command object.
#    Should produce a Result object when executed (e.g., success/failure, log, message).

# Design 
#an abstract Command base class and one or two concrete implementations (e.g., StartCoffeeMachineCommand, TurnOffLightsCommand).
# Design a Result class that stores:
# Status: "success" / "failure"
# Optional message
# Implement an Invoker or CommandExecutor that:
# Accepts a Command instance
# Calls its execute() method
# Returns a Result
# Provide a basic driver to simulate execution of a few commands.

from abc import ABC, abstractmethod
class Result:
    def __init__(self,status,message) -> None:
        self.status = status
        self.message = message
    def __str__(self) -> str:
        return f"{self.status.upper()} {self.message}"
        
    
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class StartCoffeeMachineCommand(Command):
    def execute(self):
        return Result("success","[StartCoffeeMachineCommand] strated")

class TurnOffLightsCommand(Command):
    def execute(self):
        return Result("success", "[TurnOffLightsCommand] turned off")
    
#invoker
class Invoker:
    def run_command(self,command):
        try:
            result = command.execute()
            return result
        except Exception as e:
            return Result("failure",f"Method not executed {str(e)}")

class Fail(Command):
    def execute(self):
        raise RuntimeError("This command is intentionally broken.")
        
if __name__ == "__main__":
    executor = Invoker()

    commands = [
        StartCoffeeMachineCommand(),
        TurnOffLightsCommand(),
        Fail()
    ]

    for command in commands:
        result = executor.run_command(command)
        print(result)
    

    


