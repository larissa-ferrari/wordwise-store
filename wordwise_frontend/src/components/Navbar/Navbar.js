import React from 'react';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar-container">
      <div className="logo">WORDWISE</div>
      <ul className="nav-links">
        <li><a href="/">HOME</a></li>
        <li><a href="/about">GÊNEROS</a></li>
        <li><a href="/about">AUTORES</a></li>
        <li><a href="/about">EBOOKS</a></li>
        <li><a href="/about">AUDIOBOOKS</a></li>
        <li><a href="/about">CONTATO</a></li>
        <li><a href="/about">LOGIN</a></li>
        <li><a href="/about"><span role="img" aria-label="busca">🔍</span></a></li>
      </ul>
    </nav>
  );
}

export default Navbar;
