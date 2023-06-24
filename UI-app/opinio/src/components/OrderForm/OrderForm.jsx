import React, { useState } from 'react';
import styles from './OrderForm.module.css';

const OrderForm = ({ isOpen, isYesOrder, onClose, onSubmit }) => {
    const [quantity, setQuantity] = useState('');
    const [price, setPrice] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(quantity, price);
    };

    if (!isOpen) {
        return null;
    }

    return (
        <div className={styles.modal}>
            <div className={styles.modalContent}>
                <div className={styles.modalHeader}>
                    <h3>{isYesOrder ? 'YES' : 'NO'} Order</h3>
                    <span className={styles.modalCloseButton} onClick={onClose}>&times;</span>
                </div>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="quantity">Quantity:</label>
                        <input
                            type="number"
                            id="quantity"
                            value={quantity}
                            onChange={(e) => setQuantity(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="price">Price:</label>
                        <input
                            type="number"
                            id="price"
                            value={price}
                            onChange={(e) => setPrice(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit">Place Order</button>
                </form>
            </div>
        </div>
    );
};

export default OrderForm;
