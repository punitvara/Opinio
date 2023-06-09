from question import Question
from user import User
from order import Trade
from market import Market
from market_manager import MarketManager

# Create a question
question = Question(1, "Will India win against England?")

# Create users
user1 = User(1)
user2 = User(2)

# Add money to user wallets
user1.make_deposit(1000)
user2.make_deposit(1000)

# Display user balances
print(f"User 1 balance: {user1.wallet.balance}")
print(f"User 2 balance: {user2.wallet.balance}")

# Create a market and add the trades
market = Market()

# Place trades

user1.place_order(question.q_id, 'buy', 10, 5, user1)
user2.place_order(question.q_id, 'sell', 5, 4, user2)

market.add_trade(trade1)
market.add_trade(trade2)

# Simulate settlement
question_result = "yes"  # Assume the result is "yes" for this example
winning_trades = [trade for trade in market.trades if trade.side == question_result]
for trade in winning_trades:
    user = User(trade.user_id)
    amount = trade.quantity * trade.price
    user.wallet.add(amount)

# Display user balances
print(f"User 1 balance: {user1.wallet.balance}")
print(f"User 2 balance: {user2.wallet.balance}")

# Get the average price for the question
average_price = market.get_price_for_question(question.q_id)
print(f"Average price for Question {question.q_id}: {average_price}")
