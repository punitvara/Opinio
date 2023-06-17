import React from 'react';

const Question = ({ description, onYes, onNo }) => {
    return (
        <div className="question">
            <p>{description}</p>
            <button className="yes-button" onClick={onYes}>YES</button>
            <button className="no-button" onClick={onNo}>NO</button>
        </div>
    );
};

export default Question;
