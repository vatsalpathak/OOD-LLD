"""
Problem: Alexa Device Battery Level

Objective:
Design a system for Amazon Alexa devices (e.g., Echo Show, Echo Dot) that:
1. Supports different types of inputs and outputs based on device capabilities.
2. Handles both battery-powered and plug-in (wall) powered modes.
3. Responds correctly to user queries like "check battery" by giving:
    - Battery % if battery-powered.
    - Charging status if charging.
    - A message saying it's plugged in if wall-powered.

Constraints:
- Follow OOP.
- Use Strategy Pattern for input/output behavior.
"""

from abc import ABC, abstractmethod
from enum import Enum


# Enum for power source
class PowerSource(Enum):
    BATTERY = "battery"
    WALL = "wall"

# Enum for charging state
class ChargingState(Enum):
    CHARGING = "charging"
    NOT_CHARGING = "not charging"
    PLUGGED = "plugged in"

# Strategy interface for input
class InputStrategy(ABC):
    @abstractmethod
    def take_input(self, message):
        pass

    @abstractmethod
    def is_type(self, input_type):
        pass

# Strategy interface for output
class OutputStrategy(ABC):
    @abstractmethod
    def give_output(self, message):
        pass

# === Input Strategies ===

class VoiceInput(InputStrategy):
    def take_input(self, message):
        print("[Voice] Received message")

    def is_type(self, input_type):
        return input_type.lower() == "audio"

class PhysicalInput(InputStrategy):
    def take_input(self, message):
        print("[Physical] Received message")

    def is_type(self, input_type):
        return input_type.lower() == "text"

# === Output Strategies ===

class VoiceOutput(OutputStrategy):
    def give_output(self, message):
        print(f"[VoiceOutput] Alexa says: {message}")

class DisplayOutput(OutputStrategy):
    def give_output(self, message):
        print(f"[DisplayOutput] Alexa displays: {message}")

# === Power Manager ===

class PowerManager:
    def __init__(self, power_source):
        self.power_source = power_source
        self.battery_level = 100 if power_source == PowerSource.BATTERY else None
        self.charging_state = (
            ChargingState.NOT_CHARGING if power_source == PowerSource.BATTERY
            else ChargingState.PLUGGED
        )

    def plug(self):
        if self.power_source == PowerSource.BATTERY:
            self.charging_state = ChargingState.CHARGING

    def unplug(self):
        if self.power_source == PowerSource.BATTERY:
            self.charging_state = ChargingState.NOT_CHARGING

    def set_battery_level(self, level):
        if self.power_source == PowerSource.BATTERY:
            self.battery_level = max(0, min(100, level))

    def get_status_message(self):
        if self.power_source == PowerSource.WALL:
            return "Device is plugged into wall power."
        elif self.charging_state == ChargingState.CHARGING:
            return f"Device is charging. Battery at {self.battery_level}%."
        else:
            return f"Device is not charging. Battery at {self.battery_level}%."

# === Alexa Device Base Class ===

class AlexaDevice:
    def __init__(self, name, inputs, outputs, power_source):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.power_manager = PowerManager(power_source)

    def take_input(self, input_type, message):
        handler = None
        for inp in self.inputs:
            if inp.is_type(input_type):
                handler = inp
                break

        if not handler:
            print(f"No input handler for type '{input_type}'.")
            return

        handler.take_input(message)

        if "battery" in message.lower():
            status = self.power_manager.get_status_message()
            self.give_output(status)
        else:
            self.give_output("Executing your command.")

    def give_output(self, message):
        for out in self.outputs:
            out.give_output(message)

# === Device Variants ===

class EchoShow(AlexaDevice):
    def __init__(self):
        super().__init__(
            "Echo Show",
            [VoiceInput(), PhysicalInput()],
            [VoiceOutput(), DisplayOutput()],
            PowerSource.BATTERY
        )

class EchoDot(AlexaDevice):
    def __init__(self):
        super().__init__(
            "Echo Dot",
            [VoiceInput()],
            [VoiceOutput()],
            PowerSource.WALL
        )

# === Simulation/Test Code ===

if __name__ == "__main__":
    echo_show = EchoShow()
    echo_dot = EchoDot()

    print("\n=== Test: Echo Show (Battery Powered) ===")
    echo_show.take_input("audio", "What's the battery level?")
    echo_show.power_manager.set_battery_level(65)
    echo_show.take_input("text", "check battery")
    echo_show.power_manager.plug()
    echo_show.take_input("audio", "battery status")
    echo_show.take_input("text", "play music")

    print("\n=== Test: Echo Dot (Wall Powered) ===")
    echo_dot.take_input("audio", "check battery")
    echo_dot.take_input("audio", "what's the weather")
