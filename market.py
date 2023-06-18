from collections import deque
from trade import Trade
import time
from collections import defaultdict

class Market:
    def __init__(self):
        self.questions = {}  # key: question_id, value: Question object
        self.order_books = {}  # key: question_id, value: dict of sides, which contains dict of lists (buy and sell)
        self.trades = []  # list of Trade objects
        self._trade_callbacks = []
        self._settlement_callbacks = defaultdict(list)
        
    def register_settlement_callback(self, question_id, callback):
        self._settlement_callbacks[question_id].append(callback)

    def notify_settlement_callbacks(self, question_id, winning_outcome):
        for callback in self._settlement_callbacks[question_id]:
            callback(question_id, winning_outcome)
    
    def register_trade_callback(self, callback):
        self._trade_callbacks.append(callback)
    
    def _notify_trade_callbacks(self, trade):
        for callback in self._trade_callbacks:
            callback(trade)
            
    def get_questions(self):
        return self.questions
    
    def add_question(self, question):
        self.questions[question.q_id] = question
        self.order_books[question.q_id] = {"YES": {"buy": deque(), "sell": deque()}, "NO": {"buy": deque(), "sell": deque()}}
        return True

    def add_order(self, order):
        # Add the question_id to order_books if it doesn't exist
        if order.question_id not in self.order_books:
            self.order_books[order.question_id] = {"YES": {"buy": deque(), "sell": deque()}, "NO": {"buy": deque(), "sell": deque()}}
        
        # Add the order to the appropriate order book (buy or sell)
        self.order_books[order.question_id][order.side]["buy" if order.trade_type == "buy" else "sell"].append(order)

        # Attempt to match orders
        self.match_orders(order.question_id, order.side)

    def get_liquidity(self, question_id):
        if question_id not in self.order_books:
            return {"error": "Invalid question_id"}
        
        yes_liquidity = sum(order.quantity for order in self.order_books[question_id]["YES"]["buy"]) + \
                        sum(order.quantity for order in self.order_books[question_id]["YES"]["sell"])
                        
        no_liquidity = sum(order.quantity for order in self.order_books[question_id]["NO"]["buy"]) + \
                       sum(order.quantity for order in self.order_books[question_id]["NO"]["sell"])
        
        return {"YES": yes_liquidity, "NO": no_liquidity}
    
    def match_orders(self, question_id, side):
        buy_orders = self.order_books[question_id][side]["buy"]
        sell_orders = self.order_books[question_id][side]["sell"]

        # While there are orders in both the buy and sell order books
        while buy_orders and sell_orders:
            buy_order = buy_orders[0]
            sell_order = sell_orders[0]

            # If the highest buy order price is >= the lowest sell order price
            if buy_order.price >= sell_order.price:
                print (buy_order.price, sell_order.price)
                # Execute trade
                trade_price = (buy_order.price + sell_order.price) / 2
                trade_quantity = min(buy_order.quantity, sell_order.quantity)

                # Create a trade object and add it to the trades list
                trade = Trade(buy_order.user_id, sell_order.user_id, question_id, side, trade_quantity, trade_price, time.time())
                self.trades.append(trade)
                
                # Here, instead of just logging, we call a method in MarketManager to handle the executed trade
                # market_manager.handle_executed_trade(trade)
                
                # Notify the callbacks
                self._notify_trade_callbacks(trade)

                # Update order quantities
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity

                # Remove order from order book if quantity is 0
                if buy_order.quantity == 0:
                    buy_orders.popleft()
                if sell_order.quantity == 0:
                    sell_orders.popleft()
                
                # Log the trade (in a real system, you would probably save this to a database)
                print(f"Trade executed: {trade_quantity} shares of '{side}' at ${trade_price}")

            else:
                # Orders cannot be matched
                print ("No order is matched to trade")

    def get_order_book(self, question_id, side):
        return self.order_books.get(question_id, {}).get(side, {'buy': deque(), 'sell': deque()})
