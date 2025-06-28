import React from 'react';
import './BookCard.css';

function BookCard({ title, price, image }) {
  return (
    <div className="book-card">
      <h5>{title}</h5>
      <img src={image} alt={title} />
      <p className="price">R$ {price}</p>
      <button className="buy-button">Compre agora</button>
    </div>
  );
}

export default BookCard;
