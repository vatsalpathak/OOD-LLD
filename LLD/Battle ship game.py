# Design the initial setup of a simplified Battleship game that includes:

# Requirements:
# Board:
# A grid-based game board (default 10x10).
# Can place ships on the board.
# Cannot place overlapping ships.
# Cannot place ships out of bounds.

# Ship:
# Each ship has a name (e.g., "Destroyer"), length (e.g., 3), and orientation (horizontal/vertical).
# Track which cells it occupies.

# Placement:
# Place a ship at a given coordinate (e.g., row=2, col=4) with a direction.
# Return success/failure status and message (like your Result class).
# Use OOP principles: class for Board, Ship, possibly Cell if needed.

# Constraints:
# No shooting or gameplay yet.
# Just board setup, ship placement, and collision/boundary checking.

from enum import Enum
class Orientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

class Board:
    def __init__(self,size) -> None:
        self.size = size
        self.grid = [[False for _ in range(size)] for _ in range(size)]

class Result:
    def __init__(self,status,message) -> None:
        self.status = status
        self.message = message
    def __str__(self) -> str:
        return f"{self.status.upper()} {self.message}"

class Ship:
    def __init__(self, name,length,orientation) -> None:
        self.name = name 
        self.length = length
        self.orientation = orientation
        self.positions = []

class BoardGame:
    def __init__(self,size) -> None:
        self.size = size
        self.board = Board(size)

    def _can_place(self,ship,coordinate):
        direction = ship.orientation
        row = coordinate[0]
        col = coordinate[1]
        if direction == Orientation.HORIZONTAL:
            if col + ship.length > self.size:
                return False
            for i in range(ship.length):
                if self.board.grid[row][col + i]:
                    return False
            return True
        else:
            if row + ship.length > self.size:
                return False
            for i in range(ship.length):
                if self.board.grid[row + i][col]:
                    return False
            return True

        
    def place_ship(self,ship,coordinate):
        direction = ship.orientation
        row = coordinate[0]
        col = coordinate[1]
        if not self._can_place(ship, coordinate):
            return Result("failure", f"Cannot place {ship.name} at ({row}, {col})")
        if direction == Orientation.HORIZONTAL:
            for i in range(ship.length):
                self.board.grid[row][col + i] = True
                ship.positions.append((row, col + i))
            return True
        else:
            for i in range(ship.length):
                self.board.grid[row + i][col] = True
                ship.positions.append((row + i, col))
                return True
        return Result("success", f"Placed {ship.name} at {ship.positions}")


if __name__ == "__main__":
    game = BoardGame(size=10)

    ship1 = Ship(name="Destroyer", length=3, orientation=Orientation.HORIZONTAL)
    ship2 = Ship(name="Submarine", length=4, orientation=Orientation.VERTICAL)
    ship3 = Ship(name="OverlapTest", length=3, orientation=Orientation.HORIZONTAL)

    print("--- Test 1: Place ship1 ---")
    print(game.place_ship(ship1, (0, 0)))

    print("--- Test 2: Place ship2 ---")
    print(game.place_ship(ship2, (2, 5)))

    print("--- Test 3: Try Overlapping ship3 ---")
    print(game.place_ship(ship3, (0, 1)))  # Should overlap with ship1

    print("--- Test 4: Out of bounds ---")
    ship4 = Ship(name="Oversize", length=6, orientation=Orientation.HORIZONTAL)
    print(game.place_ship(ship4, (9, 6)))  # Should go out of board
