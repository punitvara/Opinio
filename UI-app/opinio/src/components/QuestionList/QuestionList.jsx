import React from 'react';
import Question from '../Question';

const QuestionList = ({ questions, onAnswer }) => {
    return (
        <div className="question-list">
            {questions.map((question, index) => (
                <Question
                    key={index}
                    description={question.description}
                    onYes={() => onAnswer(index, true)}
                    onNo={() => onAnswer(index, false)}
                />
            ))}
        </div>
    );
};

export default QuestionList;
