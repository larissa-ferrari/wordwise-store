import React, { useState } from 'react';
import Navbar from '../../components/Navbar/Navbar';
import Footer from '../../components/Footer/Footer';
import BookCard from '../../components/BookCard/BookCard';
import './ProductList.css';

// Dados mockados
const allProducts = [
  {
    id: 1,
    title: 'Pinoquio',
    price: '54.90',
    image: require('../../assets/books/pinoquio.jpg'),
  },
  {
    id: 2,
    title: 'Em Algum Lugar nas Estrelas',
    price: '49.90',
    image: require('../../assets/books/estrelas.jpg'),
  },
  {
    id: 3,
    title: 'Alice no País das Maravilhas',
    price: '59.90',
    image: require('../../assets/books/alice.jpg'),
  },
  {
    id: 4,
    title: 'Drácula',
    price: '59.90',
    image: require('../../assets/books/dracula.jpg'),
  },
  {
    id: 5,
    title: 'O Pequeno Príncipe',
    price: '39.90',
    image: require('../../assets/books/dracula.jpg'),
  },
  {
    id: 6,
    title: '1984',
    price: '44.90',
    image: require('../../assets/books/dracula.jpg'),
  },
];

function ProductList() {
  const [currentPage, setCurrentPage] = useState(1);
  const productsPerPage = 4;

  const indexOfLastProduct = currentPage * productsPerPage;
  const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
  const currentProducts = allProducts.slice(indexOfFirstProduct, indexOfLastProduct);

  const totalPages = Math.ceil(allProducts.length / productsPerPage);

  return (
    <div>
      <Navbar />
      <div className="product-list-container">
        <h2 className="product-list-title">Todos os Livros</h2>
        <div className="product-grid">
          {currentProducts.map((book) => (
            <BookCard
              key={book.id}
              id={book.id}              
              title={book.title}
              price={book.price}
              image={book.image}
            />
          ))}
        </div>
        <div className="pagination">
          {Array.from({ length: totalPages }, (_, index) => (
            <button
              key={index + 1}
              className={currentPage === index + 1 ? 'active' : ''}
              onClick={() => setCurrentPage(index + 1)}
            >
              {index + 1}
            </button>
          ))}
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default ProductList;
