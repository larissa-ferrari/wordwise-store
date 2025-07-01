import "./Navbar.css";
import { logout } from "../../api/authApi";
import { Link } from "react-router-dom";
import { useCarrinho } from "../../contexts/cartContext";
import { isAuthenticated, getUsername } from "../../utils/auth";

function Navbar() {
    const autenticado = isAuthenticated();
    const username = getUsername();
    const { quantidadeCarrinho } = useCarrinho();

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
                <li><Link to="/">HOME</Link></li>
                <li><Link to="/livros">LIVROS</Link></li>
                {/* <li><Link to="/livros?categoria=romance">GÊNEROS</Link></li>
                <li><Link to="/livros?autor=Machado">AUTORES</Link></li> */}
                <li><Link to="/livros?tipo=ebook">EBOOKS</Link></li>
                <li><Link to="/livros?tipo=audiobook">AUDIOBOOKS</Link></li>
                <li><Link to="/contato">CONTATO</Link></li>
                <li><Link to="/carrinho">🛒 Carrinho ({quantidadeCarrinho})</Link></li>
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
