import React from "react";
import "./Navbar.css";
import { logout, isAuthenticated, getUsername } from "../../api/authApi";

function Navbar() {
  const autenticado = isAuthenticated();
  const username = getUsername();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (err) {
      console.error("Erro ao fazer logout:", err);
    }
  };

  return (
    <nav className="navbar-container">
      <div className="logo">WORDWISE</div>
      <ul className="nav-links">
        <li>
          <a href="/">HOME</a>
        </li>
        <li>
          <a href="/about">GÊNEROS</a>
        </li>
        <li>
          <a href="/about">AUTORES</a>
        </li>
        <li>
          <a href="/about">EBOOKS</a>
        </li>
        <li>
          <a href="/about">AUDIOBOOKS</a>
        </li>
        <li>
          <a href="/about">CONTATO</a>
        </li>
        {autenticado ? (
          <>
            <li>
              <a href="#" onClick={handleLogout}>
                LOGOUT
              </a>
            </li>
            <li>
              Bem-vindo, <strong>{username}</strong>
            </li>
          </>
        ) : (
          <li>
            <a href="/login">LOGIN</a>
          </li>
        )}

        <li>
          <a href="/about">
            <span role="img" aria-label="busca">
              🔍
            </span>
          </a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
