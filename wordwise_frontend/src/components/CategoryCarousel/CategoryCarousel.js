import React from 'react';
import './CategoryCarousel.css';
import lancamentosImg from '../../assets/categories/lancamentos.jpg';
import maisVendidosImg from '../../assets/categories/mais-vendidos.jpg';
import promocoesImg from '../../assets/categories/promocoes.jpg';
import boxImg from '../../assets/categories/box.jpg';

const categories = [
  { name: 'LANÇAMENTOS', image: lancamentosImg },
  { name: 'MAIS VENDIDOS', image: maisVendidosImg },
  { name: 'PROMOÇÕES', image: promocoesImg },
  { name: 'BOX E COLEÇÕES', image: boxImg }
];

function CategoryCarousel() {
  return (
    <section className="carousel-section">
      <div className="category-carousel">
        {categories.map((cat, index) => (
          <div className="category-item" key={index}>
            <img src={cat.image} alt={cat.name} />
            <p>{cat.name}</p>
          </div>
        ))}
      </div>
      <div className="carousel-indicators">
        {categories.map((_, i) => (
          <span key={i} className={`dot ${i === 0 ? 'active' : ''}`} />
        ))}
      </div>
    </section>
  );
}

export default CategoryCarousel;
