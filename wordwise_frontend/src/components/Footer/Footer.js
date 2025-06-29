import React from 'react';
import './Footer.css';
import { FaFacebookF, FaInstagram, FaPinterestP, FaTwitter, FaYoutube } from 'react-icons/fa';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-column">
          <h4>WORDWISE</h4>
          <ul>
            <li>Sobre nós</li>
            <li>Nossos serviços</li>
            <li>Políticas de privacidade</li>
            <li>Podcast</li>
          </ul>
        </div>

        <div className="footer-column">
          <h4>Ajuda</h4>
          <ul>
            <li>FAQ</li>
            <li>Entrega</li>
            <li>Devolução</li>
            <li>Acompanhar pedido</li>
            <li>Opções de pagamento</li>
          </ul>
        </div>

        <div className="footer-column">
          <h4>Explore</h4>
          <ul>
            <li>Livros</li>
            <li>Gêneros</li>
            <li>Autores</li>
            <li>Ebooks</li>
            <li>Audiobooks</li>
          </ul>
        </div>

        <div className="footer-column social">
          <h4>Nos siga</h4>
          <div className="social-icons">
            <a href="#"><FaFacebookF /></a>
            <a href="#"><FaInstagram /></a>
            <a href="#"><FaPinterestP /></a>
            <a href="#"><FaTwitter /></a>
            <a href="#"><FaYoutube /></a>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        © 2025 Wordwise. Todos os direitos reservados.
      </div>
    </footer>
  );
}

export default Footer;
