from fastapi import FastAPI, WebSocket, HTTPException, Depends
from pydantic import BaseModel
from market import Market
from market_manager import MarketManager
from user import User
from roles import UserRole
import time
from order import Order
from outcome import Outcome
import socketio
from fastapi.middleware.cors import CORSMiddleware

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
app = FastAPI()
socket_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)



# Enable CORS
origins = [
    "http://localhost:3000", # React's default port
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create market instance
market = Market()

# Create MarketManager instance with the market
market_manager = MarketManager(market)

# Create an admin user
admin_user = User(user_id=1, user_role=UserRole.ADMIN)
market_manager.register_user(admin_user)


class QuestionInput(BaseModel):
    question: str
    initial_yes_price: float
    initial_no_price: float
    liquidity_quantity: int
    question_type: str  # The new dummy input
    def print_all(self):
        print(self.question)
        print(self.initial_yes_price)
        print(self.initial_no_price)
        print(self.liquidity_quantity)
        print(self.question_type)
        
@sio.event
async def connect(sid, environ):
     print('Client connected', sid)

@sio.event
async def disconnect(sid):
    print('Client disconnected', sid)

@app.post("/create_question/")
async def create_question(input: QuestionInput):
    # Admin creates a question and gets its ID
    question_id = admin_user.create_question(market_manager, input.question)
    outcome = Outcome(question_id)
    outcome.set_price_yes(input.initial_yes_price)
    outcome.set_price_no(input.initial_no_price)
    obj = market_manager.get_question_object(question_id)
    obj.set_outcomes(outcome)
    market_manager.register_event_settlement_callback(question_id)
    
    # Add Liquidity to the market for the question
    market.add_order(Order(1, question_id, 'sell', input.liquidity_quantity, 'YES', input.initial_yes_price, time.time()))
    market.add_order(Order(1, question_id, 'sell', input.liquidity_quantity, 'NO', input.initial_no_price, time.time()))
    
    
    # Construct the details of the new question for frontend
    new_question_details = {
        "question_id": question_id,
        "question_text": input.question,
        "outcome_prices": {
            "yes": input.initial_yes_price,
            "no": input.initial_no_price
        }
    }
    # Notify clients that a new question is added
    await sio.emit('new_question', new_question_details)
    
    return {"question_id": question_id}


@app.get("/questions/")
async def get_questions():
    # Retrieve all questions
    questions = market.get_questions()
    return questions


@app.get("/questions_details/")
async def get_questions_details():
    # Retrieve all questions with their details
    questions_objects = market.get_questions() # I assume this returns a list of question objects
    questions_details = []
    for _, question in questions_objects.items():
        question_details = {
            "question_id": question.q_id, # Replace with the appropriate attribute for question ID
            "question_text": question.q_text, # Replace with the appropriate attribute for question text
            "outcome_prices": {
                "yes": question.outcomes.get_price_yes(), # Replace with the appropriate method to get the YES price
                "no": question.outcomes.get_price_no() # Replace with the appropriate method to get the NO price
            }
        }
        questions_details.append(question_details)
    
    return {"questions": questions_details}