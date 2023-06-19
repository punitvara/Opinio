import React, { useState } from 'react';
import styles from './CreateQuestionPage.module.css';

const CreateQuestionPage = ({ onQuestionCreated }) => {
  const [formData, setFormData] = useState({
    question: '',
    initial_yes_price: '',
    initial_no_price: '',
    liquidity_quantity: '',
    question_type: '',
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    console.log('handleSubmit called');
    event.preventDefault();

    // Send POST request to localhost:8000/create_question
    console.log('Making fetch call to create question');
    fetch('http://localhost:8000/create_question', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (response.ok) {
          // Handle successful response
          console.log('Question created successfully!');
          // Call the callback function to re-fetch the questions
          if (onQuestionCreated) {
            console.log('Calling onQuestionCreated callback');
            onQuestionCreated();
            setTimeout(onQuestionCreated, 1000);
          }
        } else {
          // Handle error response
          console.error('Failed to create question.');
        }
      })
      .catch((error) => {
        // Handle any errors during the request
        console.error('Error creating question:', error);
      });
  };

  return (
    <div className={styles.container}>
      <h1>Create Question</h1>
      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.formGroup}>
          <label htmlFor="question">Question:</label>
          <input
            type="text"
            id="question"
            name="question"
            value={formData.question}
            onChange={handleChange}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="initial-yes-price">Initial Yes Price:</label>
          <input
            type="number"
            id="initial-yes-price"
            name="initial_yes_price"
            value={formData.initial_yes_price}
            onChange={handleChange}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="initial-no-price">Initial No Price:</label>
          <input
            type="number"
            id="initial-no-price"
            name="initial_no_price"
            value={formData.initial_no_price}
            onChange={handleChange}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="liquidity-quantity">Liquidity Quantity:</label>
          <input
            type="number"
            id="liquidity-quantity"
            name="liquidity_quantity"
            value={formData.liquidity_quantity}
            onChange={handleChange}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="question-type">Question Type:</label>
          <input
            type="text"
            id="question-type"
            name="question_type"
            value={formData.question_type}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default CreateQuestionPage;
