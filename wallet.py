class Wallet:
    def __init__(self, id) -> None:
        self.id = id
        self.balance = 0
        self.promotional_balance = 0
    
    def get_balance(self):
        return self.balance + self.promotional_balance
    
    def add(self, amount):
        self.balance += amount
        return self
    
    def substract(self, amount):
        self.balance -= amount
        return self