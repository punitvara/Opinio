import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import QuestionList from './components/QuestionList';
import CreateQuestionPage from './components/CreateQuestionPage';

const App = () => {
  const [questions, setQuestions] = useState([]);
  const fetchQuestions = () => {
    console.log('fetchQuestions called');
    fetch('http://localhost:8000/questions_details/')
        .then(response => response.json())
        .then(data => {
            console.log('Raw data from the backend:', data); // For debugging
            const fetchedQuestions = data.questions.map(q => ({ // Notice the change here
                description: q.question_text,
                yesPrice: q.outcome_prices.yes,
                noPrice: q.outcome_prices.no
            }));
            console.log('Updating questions state with:', fetchedQuestions); // Add this line
            setQuestions(fetchedQuestions);
        })
        .catch(error => console.error('Error fetching questions:', error));
};

useEffect(fetchQuestions, []);
// Uncomment this line to rerender the questions automatically.
  // useEffect(fetchQuestions, [questions]);

  // Second useEffect to log when the state is updated
  // useEffect(() => {
  //   console.log('Questions state updated, component re-rendered:', questions);
  // }, [questions]);


  const handleAnswer = (index, answer) => {
    console.log(`Question ${index + 1} answered ${answer ? "YES" : "NO"}`);
  };

  return (
    <Router>
        <div className="App">
            <Routes>
                <Route path="/" element={<QuestionList questions={questions} onAnswer={handleAnswer} />} />
                <Route path="/create-question" element={<CreateQuestionPage onQuestionCreated={fetchQuestions} />} />            </Routes>
        </div>
    </Router>
    );
};

export default App;
