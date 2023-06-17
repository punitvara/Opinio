import React from 'react';

const Question = ({ description, onYes, onNo, yesPrice, noPrice }) => {
    return (
        <div className="question">
            <p>{description}</p>
            <div>
                <button className="yes-button" onClick={onYes}>{`YES (${yesPrice})`}</button>
                <button className="no-button" onClick={onNo}>{`NO (${noPrice})`}</button>
            </div>
        </div>
    );
};

export default Question;
