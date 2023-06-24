import React from 'react';
import Question from '../Question';

const QuestionList = ({ questions, onOrderClick }) => {
  return (
    <div>
      {questions.map((question, index) => (
        <Question
          key={index}
          description={question.description}
          onOrderClick={(isYesOrder) => onOrderClick(isYesOrder, index)}
          yesPrice={question.yesPrice}
          noPrice={question.noPrice}
        />
      ))}
    </div>
  );
};

export default QuestionList;
