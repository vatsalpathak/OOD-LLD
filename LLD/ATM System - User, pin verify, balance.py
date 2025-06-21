# Question – Part 2: Add User Authentication and User Balance
# Extend your ATM system to support basic user accounts.
#
# Your system should:
# - Allow adding users with PIN and balance.
# - Allow users to log in using user ID and PIN.
# - Only allow withdrawals from the ATM *if the user is logged in and has sufficient balance*.
# - Deduct the withdrawn amount from the user’s account.
#
# Constraints:
# - Track user sessions (i.e., who is currently logged in).
# - Keep user balances in memory (no persistence needed).
# - Prevent ATM withdrawal if either:
#     - The user’s balance is insufficient, OR
#     - The ATM can’t dispense that amount.
#
# Think about:
# - Separating ATM cash logic from user logic.
# - How to structure classes so logic doesn't mix responsibilities.
# - Clean interface for login, logout, withdraw.

class User:
    def __init__(self, user_id, pin, balance):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance

    def deduct_balance(self, amount):
        self.balance -= amount

    def __str__(self):
        return f"User({self.user_id}, Balance: {self.balance})"


class UserManager:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def add_user(self, user: User):
        self.users[user.user_id] = user

    def login(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.pin == pin:
            self.current_user = user
            return f"Login successful for user: {user_id}"
        return "Invalid credentials"

    def logout(self):
        self.current_user = None
        return "Logged out successfully"

    def get_logged_in_user(self):
        return self.current_user


class ATM:
    def __init__(self, denomination_100, denomination_500, denomination_1000):
        self.denomination = {
            1000: denomination_1000,
            500: denomination_500,
            100: denomination_100
        }

    def load_cash(self, denomination, count):
        if denomination not in self.denomination:
            raise ValueError("Unsupported denomination")
        self.denomination[denomination] += count

    def check_balance(self):
        return sum(denom * count for denom, count in self.denomination.items())

    def _can_dispense(self, amount):
        to_dispense = {}
        remaining = amount
        for denom in sorted(self.denomination.keys(), reverse=True):
            if remaining <= 0:
                break
            available = self.denomination[denom]
            needed = remaining // denom
            use = min(available, needed)
            if use > 0:
                to_dispense[denom] = use
                remaining -= denom * use
        return to_dispense if remaining == 0 else None

    def withdraw(self, amount):
        to_dispense = self._can_dispense(amount)
        if not to_dispense:
            return None
        for denom, count in to_dispense.items():
            self.denomination[denom] -= count
        return to_dispense

    def status(self):
        return f"Available Notes: {self.denomination}, Total: {self.check_balance()}"


class ATMService:
    def __init__(self, atm: ATM, user_manager: UserManager):
        self.atm = atm
        self.user_manager = user_manager

    def withdraw(self, amount):
        user = self.user_manager.get_logged_in_user()
        if not user:
            return "No user logged in"

        if user.balance < amount:
            return f"Insufficient balance: {user.balance}"

        if self.atm.check_balance() < amount:
            return f"ATM has insufficient cash"

        dispensed = self.atm.withdraw(amount)
        if dispensed:
            user.deduct_balance(amount)
            return f"Withdrawal successful. Dispensed: {dispensed}"
        return "Cannot dispense the exact amount with available denominations"


# Test the system
if __name__ == "__main__":
    atm = ATM(10, 2, 1)
    users = UserManager()
    users.add_user(User("u1", "1234", 3000))
    users.add_user(User("u2", "5678", 500))

    service = ATMService(atm, users)

    print(users.login("u1", "1234"))
    print(service.withdraw(1600))  # Should succeed
    print(service.withdraw(2000))  # Should fail - user doesn't have enough now
    print(atm.status())
    print(users.logout())

    print(users.login("u2", "5678"))
    print(service.withdraw(600))   # Should fail - user has only 500
    print(service.withdraw(400))   # May fail depending on available denominations
    print(users.logout())
