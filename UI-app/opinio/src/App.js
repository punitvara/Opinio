import React, { useState } from 'react';
import './App.css';
import QuestionList from './components/QuestionList';

const App = () => {
    const [questions] = useState([
        { description: "India to win the match vs Australia ?" },
        { description: "India to score 42 or more runs by 8.0 overs ?" }
    ]);

    const handleAnswer = (index, answer) => {
        console.log(`Question ${index + 1} answered ${answer ? "YES" : "NO"}`);
    };

    return (
        <div className="App">
            <QuestionList questions={questions} onAnswer={handleAnswer} />
        </div>
    );
};

export default App;
