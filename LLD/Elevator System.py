# Question
# Design a simple Elevator Controller.
#
# Your system should:
# - Represent an elevator that can move between floors.
# - Allow external requests (from floors) and internal requests (from inside elevator).
#
# Requirements:
# - Elevator starts at floor 0.
# - Support `request_floor(floor_number)` to add a floor request.
# - Support `step()` to move one floor at a time toward the next requested floor.
# - Show current direction and floor at each step.
#
# Think about:
# - How to queue and prioritize floor requests.
# - How to separate concerns like movement vs. handling requests.

from enum import Enum
import heapq

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"

class Elevator:
    def __init__(self, max_floor=10):
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.requests_up = []
        self.requests_down = []
        self.max_floor = max_floor

    def request_floor(self, floor):
        if floor == self.current_floor:
            print(f"Elevator already at floor {floor}")
            return

        if floor > self.current_floor:
            heapq.heappush(self.requests_up, floor)
        else:
            heapq.heappush(self.requests_down, -floor)  # invert for max-heap behavior

        self._update_direction()

    def _update_direction(self):
        if self.direction == Direction.IDLE:
            if self.requests_up:
                self.direction = Direction.UP
            elif self.requests_down:
                self.direction = Direction.DOWN

    def step(self):
        if self.direction == Direction.UP:
            self.current_floor += 1
            print(f"Moving UP to floor {self.current_floor}")
            if self.current_floor in self.requests_up:
                self.requests_up.remove(self.current_floor)
                print(f"Stopping at floor {self.current_floor}")
            if not self.requests_up:
                self.direction = Direction.DOWN if self.requests_down else Direction.IDLE

        elif self.direction == Direction.DOWN:
            self.current_floor -= 1
            print(f"Moving DOWN to floor {self.current_floor}")
            if -self.current_floor in self.requests_down:
                self.requests_down.remove(-self.current_floor)
                print(f"Stopping at floor {self.current_floor}")
            if not self.requests_down:
                self.direction = Direction.UP if self.requests_up else Direction.IDLE

        else:
            print("Elevator is IDLE at floor", self.current_floor)

    def status(self):
        return f"Floor: {self.current_floor}, Direction: {self.direction.value}"
    

if __name__ == "__main__":
    elevator = Elevator()

    elevator.request_floor(3)
    elevator.request_floor(1)
    elevator.request_floor(5)

    for _ in range(10):
        print(elevator.status())
        elevator.step()

