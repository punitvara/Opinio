// Question.jsx
import React from 'react';

const Question = ({ description, onOrderClick, yesPrice, noPrice }) => {
    return (
        <div className="question">
            <p>{description}</p>
            <div>
                <button className="yes-button" onClick={() => onOrderClick(true)}>{`YES (${yesPrice})`}</button>
                <button className="no-button" onClick={() => onOrderClick(false)}>{`NO (${noPrice})`}</button>
            </div>
        </div>
    );
};

export default Question;
