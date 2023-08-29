prediction_market/
├── config/
│   └── settings.py
├── data_access/
│   ├── repositories/
│   │   └── market_repository.py
│   ├── models/
│   │   ├── wallet.py
│   │   ├── user.py
│   │   ├── question.py
│   │   ├── order.py
│   │   ├── outcome.py
│   │   └── trade.py
│   └── db.py
├── services/
│   ├── market_manager.py
│   ├── market.py
│   └── user_service.py
├── presentation/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── market.py
│   │   │   └── users.py
│   │   ├── api.py
│   │   └── main.py (optional, if main.py serves as a part of the api)
│   └── frontend/
│       ├── public/
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   └── App.js
│       └── package.json
├── events/
│   ├── kafka_producer.py
│   └── kafka_consumer.py
├── utils/
│   └── roles.py
├── tests/
│   ├── data_access/
│   ├── services/
│   └── presentation/
├── docs/
└── main.py (optional, if not part of the api)


Project Structure eventually


For building MVP I am thinking of following structure.

prediction-market-app/
│
├── backend/
│   ├── kafka/
│   │   ├── __init__.py
│   │   ├── producer.py  (Kafka producer code)
│   │   └── consumer.py  (Kafka consumer code)
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py   (PostgreSQL integration)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── wallet.py
│   │   ├── question.py
│   │   ├── order.py
│   │   ├── outcome.py
│   │   ├── roles.py
│   │   └── trade.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── market_manager.py
│   │   └── market.py
│   │
│   ├── api.py  (API integration code)
│   ├── main.py (main application code)
│   └── config.py (configuration related code)
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── App.js
    ├── package.json
    └── ...

Install DB:
brew install postgresql
Start server.
brew services start postgresql


Start postgresql in command line mode:
$ psql postgres

% create New user 
CREATE USER new_username WITH PASSWORD 'new_password';

% Grant access
ALTER USER new_username CREATEDB;

% create database
CREATE DATABASE prediction_market_db;

% Now we have created the database you can access it using below URL
postgresql://username:password@localhost:5432/prediction_market_db

% Dbeaver
brew install --cask dbeaver-community