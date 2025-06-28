import React from 'react';
import BookCard from './BookCard';
import './BookHighlights.css';

import pinoquio from '../assets/pinoquio.jpg';
import estrelas from '../assets/estrelas.jpg';
import alice from '../assets/alice.jpg';
import dracula from '../assets/dracula.jpg';

const books = [
  { title: 'Pinoquio', price: '54.90', image: pinoquio },
  { title: 'Em Algum Lugar nas Estrelas', price: '49.90', image: estrelas },
  { title: 'Alice no País das Maravilhas', price: '59.90', image: alice },
  { title: 'Drácula', price: '59.90', image: dracula }
];

function BookHighlights() {
  return (
    <section className="highlight-section">
      <h2 className="highlight-title">NOVIDADES</h2>
      <div className="highlight-container">
        {books.map((book, i) => (
          <BookCard key={i} {...book} />
        ))}
      </div>
    </section>
  );
}

export default BookHighlights;
