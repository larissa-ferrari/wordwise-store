import React from 'react';
import { Link } from 'react-router-dom';
import './BookCard.css';

function BookCard({ id, title, price, image }) {
  return (
    <div className="book-card">
      <div className="book-content">
        <h5>{title}</h5>
        <img src={image} alt={title} />
        <p className="price">R$ {price}</p>
      </div>
      <Link to={`/livro/${id}`}>
        <button className="buy-button">Ver Detalhes</button>
      </Link>
    </div>
  );
}

export default BookCard;
