from wallet import Wallet
from order import Order
from time import time
from market import Market

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.wallet = Wallet(user_id)
        self.user_type = "Normal"
        self.open_orders = []
        self.closed_orders = []
        # Dictionary because each user can buy/sell Yes and No for multiple questions
        self.question_quantities = {}  # Dictionary to track question quantities
        self.question_probabilities = {}  # Dictionary to track question probabilities

    def make_deposit(self, amount):
        self.wallet.add(amount)
        return self

    def make_withdrawal(self, amount):
        if self.wallet.balance >= amount:
            self.wallet.subtract(amount)
        else:
            print("Insufficient balance.")
    
    def display_user_balance(self):
        print(f"{self.user_id}'s balance: ${self.balance}")
        return self

    def prepare_question(self, question):
        pass

    def post_question(self, q_id):
        pass
    
    def buy(self, question_id, trade_type, quantity, side, price):
        if self.wallet.balance >= quantity * price:
            order = Order(user_id=self.user_id, question_id=question_id, trade_type=trade_type,
                      quantity=quantity, price=price)
            self.open_orders.append(order)
            market.add_order(order)
            
            trade = Trade(self.user_id, question_id, trade_type, quantity, side, price, time.time())
            self.status = "Open"
            user.wallet.subtract(quantity * price)
            return True
        else:
            return False
        
    def sell(self):
        pass
    
    def place_order(self, question_id, trade_type, quantity, price):
        if trade_type == "buy":
            success = self.buy(question_id, trade_type, quantity, price)
        else:
            success = self.sell()
            
        
        if success == True:
            self.order_id = generate_order_id()  # Implement a method to generate a unique order ID
            