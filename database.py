from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, declarative_base
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import uuid
from fastapi import Depends

# Configuration
DATABASE_URL = "postgresql://punit:4321@localhost/prediction_market_db"

# Create an engine to the database
engine = create_engine(DATABASE_URL)

# Create a SessionLocal instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use scoped_session to ensure that one session is used per thread
# session_factory = sessionmaker(bind=engine)
# Session = scoped_session(session_factory)

# Base class to be used for the models
Base = declarative_base()

# Define User table
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    role = Column(String(255))
    balance = Column(Float)

    wallet = relationship("Wallet", uselist=False, back_populates="user")
    open_orders = relationship("Order", backref="user", foreign_keys="[Order.user_id]")
    closed_orders = relationship("Order", backref="user", foreign_keys="[Order.user_id]")

    question_quantities = relationship("Position", backref="user")
    question_probabilities = relationship("Probability", backref="user")

# Define Question table
class Question(Base):
    __tablename__ = 'questions'

    q_id  = Column(Integer, primary_key=True)
    q_text = Column(Text)
    creator_user_id = Column(Integer, ForeignKey('users.user_id'))
    timestamp = Column(String(255))

    creator = relationship("User")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.q_id'), nullable=False)
    trade_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    side = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, nullable=False, default='pending')
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

# Define Wallet table
class Wallet(Base):
    __tablename__ = 'wallets'

    wallet_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    balance = Column(Float)
    promotional_balance = Column(Float)

    user = relationship("User", back_populates="wallet")

# Define Position table
class Position(Base):
    __tablename__ = 'positions'

    position_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    question_id = Column(Integer, ForeignKey('questions.q_id'))
    quantity_yes = Column(Float)
    quantity_no = Column(Float)

    user = relationship("User", back_populates="positions")
    question = relationship("Question")

# Define Outcome table
class Outcome(Base):
    __tablename__ = 'outcomes'

    outcome_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.q_id'))
    outcome_yes_price = Column(Float)
    outcome_no_price = Column(Float)

    question = relationship("Question")

# Function to create the tables in the database
def create_tables():
    Base.metadata.create_all(engine)

# Function to drop the tables from the database
def drop_tables():
    Base.metadata.drop_all(engine)
    
# You can add more functions to interact with the database here (e.g. CRUD operations)
def create_user(db: SessionLocal, role, balance, user_type):
    user = User(role=role, balance=balance, user_type=user_type)
    db.add(user)
    
    # After adding the user, we also create a wallet for them.
    wallet = Wallet(user_id=user.user_id, balance=balance)
    db.add(wallet)
    
    db.commit()
    return user

def get_user(db: SessionLocal, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user

def update_user(db: SessionLocal, user_id: int, **kwargs):
    user = db.query(User).get(user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    return user

def delete_user(db: SessionLocal, user_id: int):
    user = db.query(User).get(user_id)
    db.delete(user)
    db.commit()

def create_question(q_text, creator_user_id, timestamp):
    session = Session()
    question = Question(q_text=q_text, creator_user_id=creator_user_id, timestamp=timestamp)
    session.add(question)
    session.commit()
    return question

def get_question(q_id):
    session = Session()
    return session.query(Question).get(q_id)

def update_question(q_id, **kwargs):
    session = Session()
    question = session.query(Question).get(q_id)
    for key, value in kwargs.items():
        setattr(question, key, value)
    session.commit()

def delete_question(q_id):
    session = Session()
    question = session.query(Question).get(q_id)
    session.delete(question)
    session.commit()
    

def create_order(user_id, question_id, trade_type, quantity, side, price):
    session = Session()
    order = Order(user_id=user_id, question_id=question_id, trade_type=trade_type,
                  quantity=quantity, side=side, price=price)
    session.add(order)
    session.commit()
    return order

def get_order(order_id):
    session = Session()
    return session.query(Order).get(order_id)

def update_order(order_id, **kwargs):
    session = Session()
    order = session.query(Order).get(order_id)
    for key, value in kwargs.items():
        setattr(order, key, value)
    session.commit()

def delete_order(order_id):
    session = Session()
    order = session.query(Order).get(order_id)
    session.delete(order)
    session.commit()

def create_position(user_id, question_id, quantity_yes, quantity_no):
    session = Session()
    position = Position(user_id=user_id, question_id=question_id, quantity_yes=quantity_yes, quantity_no=quantity_no)
    session.add(position)
    session.commit()
    return position

def get_position(position_id):
    session = Session()
    return session.query(Position).get(position_id)

def update_position(position_id, **kwargs):
    session = Session()
    position = session.query(Position).get(position_id)
    for key, value in kwargs.items():
        setattr(position, key, value)
    session.commit()

def delete_position(position_id):
    session = Session()
    position = session.query(Position).get(position_id)
    session.delete(position)
    session.commit()
    
def create_wallet(user_id, balance, promotional_balance=0):
    session = Session()
    wallet = Wallet(user_id=user_id, balance=balance, promotional_balance=promotional_balance)
    session.add(wallet)
    session.commit()
    return wallet

def get_wallet(wallet_id):
    session = Session()
    return session.query(Wallet).get(wallet_id)

def update_wallet(wallet_id, **kwargs):
    session = Session()
    wallet = session.query(Wallet).get(wallet_id)
    for key, value in kwargs.items():
        setattr(wallet, key, value)
    session.commit()

def delete_wallet(wallet_id):
    session = Session()
    wallet = session.query(Wallet).get(wallet_id)
    session.delete(wallet)
    session.commit()
    
def create_outcome(question_id, outcome_yes_price, outcome_no_price):
    session = Session()
    outcome = Outcome(question_id=question_id, outcome_yes_price=outcome_yes_price, outcome_no_price=outcome_no_price)
    session.add(outcome)
    session.commit()
    return outcome

def get_outcome(outcome_id):
    session = Session()
    return session.query(Outcome).get(outcome_id)

def update_outcome(outcome_id, **kwargs):
    session = Session()
    outcome = session.query(Outcome).get(outcome_id)
    for key, value in kwargs.items():
        setattr(outcome, key, value)
    session.commit()

def delete_outcome(outcome_id):
    session = Session()
    outcome = session.query(Outcome).get(outcome_id)
    session.delete(outcome)
    session.commit()

# Function to close the session
def close_session():
    Session.remove()
    
    
# Test the database creation
def test_database_creation():
    create_tables()
    # Perform assertions or checks to ensure the tables were created successfully


# Test the table creation
def test_table_creation():
    drop_tables()
    # Create any necessary tables before testing
    create_tables()

    # Perform assertions or checks to ensure the individual tables were created successfully


# Test the database and table creation
def test():
    test_table_creation()

# Run the tests
test()

# Create an inspector
inspector = inspect(engine)

# Get the table names
table_names = inspector.get_table_names()

# Print the table names
for table_name in table_names:
    print(table_name)

Session.remove()
