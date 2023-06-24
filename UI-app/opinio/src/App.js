import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import socketIOClient from 'socket.io-client';
import './App.css';
import QuestionList from './components/QuestionList';
import CreateQuestionPage from './components/CreateQuestionPage';
import OrderForm from './components/OrderForm';

const ENDPOINT = 'http://localhost:8000'; // Your server URL

const App = () => {
    const [questions, setQuestions] = useState([]);
    const [isOrderFormOpen, setIsOrderFormOpen] = useState(false);
    const [currentOrderInfo, setCurrentOrderInfo] = useState({ isYesOrder: true, questionIndex: 0 });

    const fetchQuestions = async () => {
        console.log('fetchQuestions called');
        const response = fetch('http://localhost:8000/questions_details/')
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

    // const fetchQuestions = async () => {
    //     console.log('fetchQuestions called');
    //     try {
    //         const response = await fetch('http://localhost:8000/questions_details/');
    //         const data = await response.json();
    //         console.log('Raw data from the backend:', data);
    //         const fetchedQuestions = data.questions.map(q => ({
    //             description: q.question_text,
    //             yesPrice: q.outcome_prices.yes,
    //             noPrice: q.outcome_prices.no
    //         }));
    //         console.log('Updating questions state with:', fetchedQuestions);
    //         setQuestions(fetchedQuestions);
    //     } catch (error) {
    //         console.error('Error fetching questions:', error);
    //     }
    // };
    
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

    const handleOrderClick = (isYesOrder, questionIndex) => {
        setCurrentOrderInfo({ isYesOrder, questionIndex });
        setIsOrderFormOpen(true);
    };

    const handlePlaceOrder = (order) => {
        console.log('Order placed:', order);
        // handle order placement (Step 2)
    };



    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route
                        path="/"
                        element={<QuestionList questions={questions} onOrderClick={handleOrderClick} />} // <-- pass handleOrderClick
                    />
                    <Route path="/create-question" element={<CreateQuestionPage onQuestionCreated={fetchQuestions} />} />
                </Routes>
                <OrderForm
                    isOpen={isOrderFormOpen}
                    onClose={() => setIsOrderFormOpen(false)}
                    onPlaceOrder={handlePlaceOrder}
                    {...currentOrderInfo}
                />
            </div>
        </Router>
    );
};

export default App;
