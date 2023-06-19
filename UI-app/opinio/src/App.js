import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import socketIOClient from 'socket.io-client';
import './App.css';
import QuestionList from './components/QuestionList';
import CreateQuestionPage from './components/CreateQuestionPage';

const ENDPOINT = 'http://localhost:8000'; // Your server URL

const App = () => {
    const [questions, setQuestions] = useState([]);

    const fetchQuestions = () => {
        console.log('fetchQuestions called');
        fetch('http://localhost:8000/questions_details/')
            .then(response => response.json())
            .then(data => {
                console.log('Raw data from the backend:', data);
                const fetchedQuestions = data.questions.map(q => ({
                    description: q.question_text,
                    yesPrice: q.outcome_prices.yes,
                    noPrice: q.outcome_prices.no
                }));
                console.log('Updating questions state with:', fetchedQuestions);
                setQuestions(fetchedQuestions);
            })
            .catch(error => console.error('Error fetching questions:', error));
    };

    useEffect(() => {
        const socket = socketIOClient(ENDPOINT);

        socket.on('new_question', (newQuestion) => {
            console.log('New question received:', newQuestion);
            const formattedQuestion = {
                description: newQuestion.question_text,
                yesPrice: newQuestion.outcome_prices.yes,
                noPrice: newQuestion.outcome_prices.no
            };
            setQuestions(prevQuestions => [...prevQuestions, formattedQuestion]);
        });

        fetchQuestions(); // Fetch questions initially

        return () => socket.disconnect(); // Disconnect socket when component unmounts
    }, []);

    const handleAnswer = (index, answer) => {
        console.log(`Question ${index + 1} answered ${answer ? 'YES' : 'NO'}`);
    };

    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<QuestionList questions={questions} onAnswer={handleAnswer} />} />
                    <Route path="/create-question" element={<CreateQuestionPage onQuestionCreated={fetchQuestions} />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
