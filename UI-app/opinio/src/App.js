import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import QuestionList from './components/QuestionList';
import CreateQuestionPage from './components/CreateQuestionPage';

const App = () => {
  const [questions] = useState([
    { description: "Do you like programming?", yesPrice: 100, noPrice: 50 },
    { description: "Do you enjoy learning new technologies?", yesPrice: 200, noPrice: 75 }
  ]);

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
