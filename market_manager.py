from question import Question
from time import time

class MarketManager:
    def __init__(self, market):
        self.market = market
         # Register the handle_executed_trade method as a callback
        self.market.register_trade_callback(self.handle_executed_trade)
        # Keep track of users
        self.users = {}
    
    def register_user(self, user):
        """
        Register a user with the manager.
        """
        self.users[user.user_id] = user

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their user_id.
        """
        return self.users.get(user_id)

    def create_question(self, q_text):
        q_id = len(self.market.questions) + 1
        question = Question(q_id, q_text, time())
        self.market.add_question(question)
        return q_id
        
        
    def add_question(self, user, question):
        # Only admin users can add questions
        if user.user_type == 'admin':
            self.market.add_question(question)
        else:
            print("Error: Only admins can add questions.")

    def process_user_order(self, user, order):
        # Check if user has enough balance or assets to place order
        if order.trade_type == 'buy':
            required_balance = order.quantity * order.price
            if user.balance < required_balance:
                print(f"Error: Insufficient balance to place order. User balance is ${user.balance}, required balance is ${required_balance}.")
                return
        elif order.trade_type == 'sell':
            assets = user.get_assets(order.question_id, order.side)
            if assets < order.quantity:
                print(f"Error: Insufficient assets to place order. User has {assets} units, trying to sell {order.quantity} units.")
                return
                
        # If sufficient balance/assets, add order to market
        self.market.add_order(order)
        
        # Add the order to the user's open orders
        user.open_orders[order.order_id] = order
        
    def handle_executed_trade(self, trade):
        # Get the user instances for buyer and seller
        buyer = self.get_user_by_id(trade.buyer_id)  # You should have some way to retrieve user by ID, I am assuming a get_user_by_id method
        seller = self.get_user_by_id(trade.seller_id)

        # Update the buyer's position
        buyer.update_position(trade.question_id, trade.side, trade.quantity)
        buyer.wallet.subtract(trade.quantity * trade.price)

        # Update the seller's position
        seller.update_position(trade.question_id, trade.side, -trade.quantity)
        seller.wallet.add(trade.quantity * trade.price)

    def close_user_order(self, user, order):
        # Close the order for the user
        user.close_order(order)
        
        # Potentially, handle transferring funds/assets between users here.
        # In a real-world system, this would involve more complex transaction handling.
        
        
    

# class MarketManager:
#     def __init__(self, market):
#         self.market = market
        
#     def process_user_order(self, user, order):
#         # Interact with the market and process user's order.
#         is_executed = self.market.process_order(order)
#         if is_executed:
#             user.close_order(order)