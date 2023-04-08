
class Player:
    def __init__(self, name, stack, client_id, hand = [], current_wager = 0, previous_wager = 0):
        self.name = name
        self.stack = stack
        self.hand = hand
        # amount wagered in the current action
        self.current_wager = current_wager
        # amount wagered in the previous action
        self.previous_wager = previous_wager
        self.client_id = client_id

    def wager(self, amount):
        if amount > self.stack or amount < 0:
            raise Exception(f"Player {self} cannot wager {amount}.")
        self.current_wager += amount
        self.stack -= amount
     
    def update_wager(self):
        self.previous_wager += self.current_wager
        self.current_wager = 0

    def __repr__(self):
        return f"{self.name}: {self.stack}"
    
    def to_dict(self):
        return {
            'name': self.name,
            'stack': self.stack,
            'current_wager': self.current_wager,
            'previous_wager': self.previous_wager,
            'client_id': self.client_id
        }
    
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name and self.client_id == other.client_id
        return False
    
    def __hash__(self):
        return hash((self.name, self.client_id))
    
    @classmethod
    def from_dict(cls, dict):
        return cls(dict['name'], dict['stack'], dict['client_id'], current_wager = dict['current_wager'], previous_wager = dict['previous_wager'])
    