import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import QuestionList from './components/QuestionList';
import CreateQuestionPage from './components/CreateQuestionPage';

const App = () => {
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    // Fetch questions from backend
    fetch('http://localhost:8000/questions_details/') // Replace this URL with the actual URL of your backend
      .then(response => response.json())
      .then(data => {
        const fetchedQuestions = data.questions.map(q => ({
          description: q.question_text,
          yesPrice: q.outcome_prices.yes,
          noPrice: q.outcome_prices.no
        }));
        setQuestions(fetchedQuestions);
      })
      .catch(error => console.error('Error fetching questions:', error));
  }, []);

  const handleAnswer = (index, answer) => {
    console.log(`Question ${index + 1} answered ${answer ? "YES" : "NO"}`);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<QuestionList questions={questions} onAnswer={handleAnswer} />} />
          <Route path="/create-question" element={<CreateQuestionPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
