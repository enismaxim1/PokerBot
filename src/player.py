
class Player:
    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hand = []
        self.current_wager = 0

    def wager(self, amount):
        if amount > self.stack or amount < 0:
            raise Exception(f"Player {self} cannot wager {amount}.")
        self.current_wager += amount
        self.stack -= amount

    def __repr__(self):
        return f"{self.name}: {self.stack}"