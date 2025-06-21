# Question – Part 1: Basic ATM Cash Withdrawal
# Design a simplified ATM Machine to handle basic cash withdrawal.
#
# Your system should:
# - Represent cash in different denominations (e.g. 100, 500, 2000).
# - Allow loading the ATM with a certain number of notes of each denomination.
# - Allow users to withdraw cash (e.g. withdraw(1300)) if the ATM has the correct denominations.
#
# Constraints:
# - Dispense highest denominations first (greedy approach).
# - If exact amount cannot be dispensed, the withdrawal should fail.
# - Track remaining cash in the ATM.
#
# Think about:
# - How to represent denominations.
# - A clean class structure that can be extended in future (e.g., logging, user accounts).
# - Where logic for dispensing should reside.


class ATM:
    def __init__(self, denomination_100,denomination_500,denomination_1000) -> None:
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
    
    def withdraw(self, amount):
        if amount > self.check_balance():
            return "Insufficient funds in ATM"
        
        to_dispense = {}
        remaining = amount

        for denom in sorted(self.denomination.keys(), reverse=True):
            if remaining <= 0:
                break

            available_notes = self.denomination[denom]
            needed_notes = remaining // denom

            used_notes = min(available_notes, needed_notes)

            if used_notes > 0:
                to_dispense[denom] = used_notes
                remaining -= denom * used_notes

        if remaining == 0:
            for denom, count in to_dispense.items():
                self.denomination[denom] -= count
            return f"Dispensed: {to_dispense}"
        else:
            return "Cannot dispense the exact amount with available denominations"
        
    def status(self):
        return f"Available Notes: {self.denomination}, Total: {self.check_balance()}"
    

if __name__ == "__main__":
    atm = ATM(denomination_100=10, denomination_500=2, denomination_1000=1)

    print(atm.status())                     # Show current status
    print(atm.withdraw(1600))              # Should succeed (1000 + 500 + 100)
    print(atm.status())
    print(atm.withdraw(1200))              # May fail depending on remaining notes
    atm.load_cash(500, 1)                  # Load more cash
    print(atm.withdraw(1200))              # Try again
