from wallet import Wallet
from order import Order
from time import time
from roles import UserRole, UserPermission, ROLE_PERMISSIONS

class User:
    def __init__(self, user_id, user_role=UserRole.NORMAL):
        self.user_id = user_id
        self.role = user_role
        self.permissions = ROLE_PERMISSIONS.get(user_role, [])
        self.wallet = Wallet(user_id)
        self.balance = self.wallet.get_balance()
        self.user_type = "Normal"
        self.open_orders = {} # Dictionary to track open orders
        self.closed_orders = {} # Dictionary to track closed orders
        # Dictionary because each user can buy/sell Yes and No for multiple questions
        self.question_quantities = {}  # Dictionary to track question quantities
        self.question_probabilities = {}  # Dictionary to track question probabilities
    
    def get_assets(self, question_id, side):
        return self.question_quantities[question_id][side]
        
    def get_position_quantity(self, question_id, side):
            # Return the quantity of a specific position ('YES' or 'NO') for a specific question
        return self.question_quantities.get(question_id, {}).get(side, 0)
    
    def update_position(self, question_id, side, quantity):
        # Update the user's position for a specific question and side ('YES' or 'NO')
        if question_id not in self.question_quantities:
            self.question_quantities[question_id] = {'YES': 0, 'NO': 0}
        self.question_quantities[question_id][side] += quantity
    
    def has_permission(self, permission):
        return permission in self.permissions
    
    def make_deposit(self, amount):
        self.wallet.add(amount)
        return self

    def make_withdrawal(self, amount):
        if self.wallet.balance >= amount:
            self.wallet.subtract(amount)
        else:
            print("Insufficient balance.")
    
    def display_user_balance(self):
        self.balance = self.wallet.get_balance()
        print(f"{self.user_id}'s balance: ${self.balance}")
        return self
    
    def create_question(self, market_manager, q_text):
        if self.has_permission(UserPermission.CREATE_QUESTION):
            q_id = market_manager.create_question(q_text)
            return q_id
        else:
            print("You do not have permission to create questions.")
    
    def post_question(self, q_id):
        pass
        
    def sell(self):
        pass
    
    def place_order(self, market_manager, question_id, trade_type, quantity, side, price):
        self.display_user_balance()
        # Create an order
        order = Order(self.user_id, question_id, trade_type, quantity, side, price, time())
        # Add the order to the open orders list
        self.open_orders[order.order_id] = order  # Add the order to the dictionary using order id
        # MarketManager will process the order
        market_manager.process_user_order(self, order)
    
    def close_order(self, order):
        # Remove order from open orders
        self.open_orders.pop(order.order_id, None)
        # Add order to closed orders
        self.closed_orders[order.order_id] = order  # Add the order to the dictionary using order id