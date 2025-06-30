import React, { useState, useEffect } from 'react';
import BookCard from '../BookCard/BookCard';
import './BookHighlights.css';
import { listarLivrosDestaque } from '../../api/bookApi';

function BookHighlights() {
    const [books, setBooks] = useState([]);

    useEffect(() => {
        const fetchHighlights = async () => {
            try {
                const data = await listarLivrosDestaque();
                setBooks(data);
            } catch (err) {
                console.error('Erro ao buscar destaques:', err);
            }
        };

        fetchHighlights();
    }, []);

    return (
        <section className="highlight-section">
            <h2 className="highlight-title">DESTAQUES</h2>
            <div className="highlight-container">
                {books.map((book) => (
                    <BookCard
                        key={book.id}
                        id={book.id}
                        title={book.titulo}
                        price={book.preco}
                        image={book.imagem_url}
                    />
                ))}
            </div>
        </section>
    );
}

export default BookHighlights;