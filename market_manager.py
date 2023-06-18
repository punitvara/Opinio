from question import Question
from time import time

class MarketManager:
    def __init__(self, market):
        self.market = market
         # Register the handle_executed_trade method as a callback
        self.market.register_trade_callback(self.handle_executed_trade)
        # Keep track of users
        self.users = {}
    def get_question_object(self, question_id):
        return self.market.questions[question_id]
    
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
    def register_event_settlement_callback(self, question_id):
        """
        Registers a callback function for event settlement.
        """
        self.market.register_settlement_callback(question_id, self.handle_event_settlement)

    def handle_event_settlement(self, question_id, winning_outcome):
        """
        Handles event settlement by distributing funds to users who hold shares of the winning outcome.
        """
        # Get the question object from the market
        question = self.market.questions.get(question_id)
        if not question:
            print(f"Question {question_id} not found.")
            return
        
        # Calculate the total quantity of the winning outcome in the market
        total_winning_quantity = sum(
            order.quantity for order in self.market.get_order_book(question_id, winning_outcome)["buy"]
        )
        
        if total_winning_quantity == 0:
            print("No winning bets found.")
            return
        
        # Calculate the winning payout per unit
        payout_per_unit = 10 / total_winning_quantity
        
        # Iterate over the users and distribute the funds
        for user_id, user in self.users.items():
            # Get the user's position quantity for the winning outcome
            position_quantity = user.get_position_quantity(question_id, winning_outcome)
            
            if position_quantity > 0:
                # Calculate the user's payout based on their position quantity
                payout = payout_per_unit * position_quantity
                
                # Update the user's balance
                user.make_deposit(payout)
                
                print(f"User {user_id} received a payout of ${payout} for question {question_id} ({winning_outcome}).")

    
    def check_and_settle_event(self, question_id, winning_outcome):
        """
        Checks if an event is over and triggers the settlement callback if it is.
        """
        # Implement the logic to check if an event is over
        # For the sake of this example, let's say you have this information available.
        # In practice, you will need a reliable way to determine this.

        event_is_over = True  # You need to determine this based on real data

        if event_is_over:
            self.market.notify_settlement_callbacks(question_id, winning_outcome)