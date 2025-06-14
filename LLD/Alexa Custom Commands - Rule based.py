# Design a system for Alexa that supports custom user-defined commands like:

# “Start coffee machine”
# “Turn off all lights”

# Each command:
#    Should be encapsulated as a Command object.
#    Should produce a Result object when executed (e.g., success/failure, log, message).

# Define an abstract Rule class with:

# evaluate() method returning True or False
# Optional reason or message
# Allow commands to have zero or more rules (via constructor or method).
# Before executing, the command should check all its rules.
# If any rule fails, the command should return a failure Result.
# Implement at least 1 or 2 example rules, e.g.:
# TimeWindowRule: Only allow command between 6AM and 10AM.
# UserPermissionRule: Allow command only for certain users.
# Modify execute() so that:
# It first checks rules.
# If rules pass → proceed with normal execution.
# If rules fail → return Result("failure", reason).

from abc import ABC, abstractmethod
import datetime

class Rule(ABC):
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def reason(self):
        pass

class TimeWindowRule(Rule):
    def __init__(self, start_hour, end_hour) -> None:
        self.start_hour = start_hour
        self.end_hour = end_hour

    def evaluate(self):
        now = datetime.datetime.now().hour
        return self.start_hour <= now <  self.end_hour
    
    def reason(self):
        return f"Command only allowed in {self.start_hour} and {self.end_hour}"
    
class UserPermissionRule(Rule):
    def __init__(self, allowed_users, current_user) -> None:
        self.allowed_users = allowed_users
        self.current_user = current_user

    def evaluate(self):
        return self.current_user in self.allowed_users
    
    def reason(self):
        return f"Command only allowed when {self.current_user} is in list of {self.allowed_users}"

class Result:
    def __init__(self,status,message) -> None:
        self.status = status
        self.message = message
    def __str__(self) -> str:
        return f"{self.status.upper()} {self.message}"
        
    
class Command(ABC):
    def __init__(self, rules=None):
        self.rules = rules if rules else []

    @abstractmethod
    def execute(self):
        pass

    def _check_rules(self):
        for rule in self.rules:
            if not rule.evaluate():
                return Result("failure", rule.reason())
        return Result("success","")
    
class StartCoffeeMachineCommand(Command):
    def execute(self):
        rule_check = self._check_rules()
        if rule_check.status == "failure":
            return rule_check
        return Result("success","[StartCoffeeMachineCommand] strated")

class TurnOffLightsCommand(Command):
    def execute(self):
        rule_check = self._check_rules()
        if rule_check.status == "failure":
            return rule_check
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

    current_hour = datetime.datetime.now().hour
    current_user = "bob"

    # Rule that should PASS (time is within range)
    time_rule_pass = TimeWindowRule(start_hour=0, end_hour=23)

    # Rule that should FAIL (user not allowed)
    user_rule_fail = UserPermissionRule(allowed_users=["admin", "alice"], current_user=current_user)

    # Rule that should PASS (user allowed)
    user_rule_pass = UserPermissionRule(allowed_users=["admin", "bob"], current_user=current_user)

    commands = [
        StartCoffeeMachineCommand(rules=[time_rule_pass, user_rule_pass]),      
        StartCoffeeMachineCommand(rules=[user_rule_fail]),                  
        TurnOffLightsCommand(),                                            
        Fail()                                                              
    ]

    for i, command in enumerate(commands, 1):
        print(f"\n--- Test #{i} ---")
        result = executor.run_command(command)
        print(result)