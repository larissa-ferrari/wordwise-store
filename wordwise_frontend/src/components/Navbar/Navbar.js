import React from "react";
import "./Navbar.css";
import { logout } from "../../api/authApi";
import { useEffect, useState } from "react";
import { obterCarrinho } from "../../api/cartApi";
import { isAuthenticated, getUsername } from "../../utils/auth";

function Navbar() {
  const autenticado = isAuthenticated();
  const username = getUsername();
  const [quantidadeCarrinho, setQuantidadeCarrinho] = useState(0);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const data = await obterCarrinho();
        const total = data.itens?.reduce(
          (acc, item) => acc + item.quantidade,
          0
        );
        setQuantidadeCarrinho(total || 0);
      } catch (err) {
        console.error("Erro ao carregar carrinho:", err);
      }
    };
    fetchCart();
  }, []);

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
          <a href="/suporte">CONTATO</a>
        </li>
        <li>
          <a href="/carrinho">🛒 Carrinho ({quantidadeCarrinho})</a>
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
