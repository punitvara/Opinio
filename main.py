from market import Market
from market_manager import MarketManager
from user import User
from roles import UserRole
import time
from order import Order

# Create market instance
market = Market()

# Create MarketManager instance with the market
market_manager = MarketManager(market)

# Create an admin user
admin_user = User(user_id=1, user_role=UserRole.ADMIN)

# Inject liquidity for the created question
initial_yes_price = 5
initial_no_price = 5
liquidity_quantity = 1000

# Admin creates a question and gets its ID
question_id = admin_user.create_question(market_manager, "Will team A win against team B?")

# Add Liquidity to the market for question
market.add_order(Order(1, question_id, 'sell', liquidity_quantity, 'YES', initial_yes_price, time.time()))

liquidity = market.get_liquidity(question_id)
print(f"Liquidity for question {question_id}: YES - {liquidity['YES']}, NO - {liquidity['NO']}")

# Create a normal user
Ramesh = User(user_id=2)

# Users deposit some funds to their wallets
Ramesh.make_deposit(1000)

Ramesh.display_user_balance()

# Normal user places a buy order for question 1
Ramesh.place_order(market_manager, question_id=question_id, trade_type="buy", quantity=10, side="YES", price=5)


liquidity = market.get_liquidity(question_id)
print(f"Liquidity for question {question_id}: YES - {liquidity['YES']}, NO - {liquidity['NO']}")


# Ramesh.place_order(market_manager, question_id=question_id, trade_type="sell", quantity=8, side="YES", price=6)

# Create a normal user
# John = User(user_id=2)

# # Users deposit some funds to their wallets
# John.make_deposit(1000)

# # Normal user places a buy order for question 1
# John.place_order(market_manager, question_id=question_id, trade_type="buy", quantity=5, side="YES", price=6)

# # Display user balances
# print(f"User 1 balance: {Ramesh.wallet.balance}")
# print(f"User 2 balance: {John.wallet.balance}")

# Simulate settlement
# question_result = "yes"  # Assume the result is "yes" for this example
# winning_trades = [trade for trade in market.trades if trade.side == question_result]
# for trade in winning_trades:
#     user = User(trade.user_id)
#     amount = trade.quantity * trade.price
#     user.wallet.add(amount)

# # Display user balances
# print(f"User 1 balance: {user1.wallet.balance}")
# print(f"User 2 balance: {user2.wallet.balance}")

# # Get the average price for the question
# average_price = market.get_price_for_question(question.q_id)
# print(f"Average price for Question {question.q_id}: {average_price}")
