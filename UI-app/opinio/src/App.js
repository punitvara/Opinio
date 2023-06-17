import React, { useState } from 'react';
import './App.css';
import QuestionList from './components/QuestionList';

const App = () => {
    const [questions] = useState([
        { description: "Do you like programming?", yesPrice: 100, noPrice: 50 },
        { description: "Do you enjoy learning new technologies?", yesPrice: 200, noPrice: 75 }
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
