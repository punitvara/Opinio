import React from 'react';
import Question from '../Question';

const QuestionList = ({ questions, onAnswer }) => {
  return (
    <div>
      {questions.map((question, index) => (
        <Question
          key={index}
          description={question.description}
          onYes={() => onAnswer(index, true)}
          onNo={() => onAnswer(index, false)}
          yesPrice={question.yesPrice}
          noPrice={question.noPrice}
        />
      ))}
    </div>
  );
};

export default QuestionList;
