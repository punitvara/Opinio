from collections import deque
from trade import Trade
import time
from collections import defaultdict

class Market:
    def __init__(self):
        self.questions = {}  # key: question_id, value: Question object
        self.order_books = {}  # key: question_id, value: dict of sides, which contains dict of lists (buy and sell)
        self.trades = []  # list of Trade objects
    def get_questions(self):
        return self.questions
    
    def add_question(self, question):
        self.questions[question.q_id] = question
        self.order_books[question.q_id] = {"YES": {"buy": deque(), "sell": deque()}, "NO": {"buy": deque(), "sell": deque()}}
        return True

    def add_order(self, order):
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
                # Execute trade
                trade_price = (buy_order.price + sell_order.price) / 2
                trade_quantity = min(buy_order.quantity, sell_order.quantity)

                # Create a trade object and add it to the trades list
                trade = Trade(buy_order.user_id, sell_order.user_id, question_id, side, trade_quantity, trade_price, time.time())
                self.trades.append(trade)
                
                # Here, instead of just logging, we call a method in MarketManager to handle the executed trade
                # market_manager.handle_executed_trade(trade)

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

# class Market:
#     def __init__(self):
#         self.orders = []
#         self.trades = []

#     def add_order(self, order):
#         self.orders.append(order)
#         self.match_orders(order)

#     def remove_order(self, order):
#         self.orders.remove(order)

#     def add_trade(self, trade):
#         self.trades.append(trade)

#     def match_orders(self, new_order):
#         matching_orders = []

#         for order in self.orders:
#             if (
#                 order.question_id == new_order.question_id
#                 and order.trade_type != new_order.trade_type
#                 and order.price == new_order.price
#             ):
#                 matching_orders.append(order)

#         for order in matching_orders:
#             if order.quantity >= new_order.quantity:
#                 self.execute_trade(new_order, order)
#                 self.remove_order(order)
#             else:
#                 self.execute_trade(new_order, order)
#                 new_order.quantity -= order.quantity
#                 self.remove_order(order)

#     def execute_trade(self, buy_order, sell_order):
#         trade_quantity = min(buy_order.quantity, sell_order.quantity)
#         trade_price = buy_order.price

#         trade = Trade(
#             buy_order.user_id,
#             sell_order.user_id,
#             buy_order.question_id,
#             trade_quantity,
#             trade_price,
#         )
#         self.add_trade(trade)

#         buy_order.quantity -= trade_quantity
#         sell_order.quantity -= trade_quantity

#         if buy_order.quantity == 0:
#             self.remove_order(buy_order)

#         if sell_order.quantity == 0:
#             self.remove_order(sell_order)


# class Market:
#     def __init__(self):
#         self.order_book = [] # List of orders # copilot was suggesting dictionary here
#         self.trades = []

#     def add_trade(self, trade):
#         self.trades.append(trade)

#     def get_trades_for_question(self, q_id):
#         return [trade for trade in self.trades if trade.q_id == q_id]

#     def get_trades_for_user(self, user_id):
#         return [trade for trade in self.trades if trade.user_id == user_id]

#     def get_total_quantity_for_question(self, q_id):
#         trades = self.get_trades_for_question(q_id)
#         total_quantity = sum(trade.quantity for trade in trades)
#         return total_quantity

#     def get_price_for_question(self, q_id):
#         trades = self.get_trades_for_question(q_id)
#         if not trades:
#             return 0

#         total_value = sum(trade.quantity * trade.price for trade in trades)
#         total_quantity = self.get_total_quantity_for_question(q_id)
#         average_price = total_value / total_quantity
#         return average_price
