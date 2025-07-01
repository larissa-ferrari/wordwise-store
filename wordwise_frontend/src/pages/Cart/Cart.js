import React, { useEffect, useState } from "react";
import { obterCarrinho, removerItemDoCarrinho } from "../../api/cartApi";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import "./Cart.css";
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { isAuthenticated } from '../../utils/auth';

function Cart() {
    const [carrinho, setCarrinho] = useState(null);
    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    useEffect(() => {
        async function carregarCarrinho() {
            try {
                const data = await obterCarrinho();
                setCarrinho(data);
            } catch (err) {
                console.error("Erro ao carregar carrinho:", err);
            } finally {
                setLoading(false);
            }
        }

        carregarCarrinho();
    }, []);

    const handleCheckout = () => {
        if (isAuthenticated()) {
            navigate('/checkout');
        } else {
            toast.warning("Você precisa estar logado para finalizar o pedido.");
            navigate('/login');
        }
    };

    const handleRemover = async (livroId) => {
        try {
            const novoCarrinho = await removerItemDoCarrinho(livroId);
            setCarrinho(novoCarrinho);
        } catch (err) {
            console.error("Erro ao remover item:", err);
        }
    };

    if (loading) {
        return (
            <div>
                <Navbar />
                <div className="cart-container">
                    <h2>Carregando...</h2>
                </div>
                <Footer />
            </div>
        );
    }

    if (!carrinho || carrinho.itens.length === 0) {
        return (
            <div>
                <Navbar />
                <div className="cart-container">
                    <h2>Seu carrinho está vazio.</h2>
                </div>
                <Footer />
            </div>
        );
    }

    const total = carrinho.itens.reduce(
        (acc, item) => acc + parseFloat(item.livro.preco) * item.quantidade,
        0
    );

    return (
        <div>
            <Navbar />
            <div className="cart-container">
                <h2>Seu Carrinho</h2>
                <ul className="cart-items">
                    {carrinho.itens.map((item) => (
                        <li key={item.id} className="cart-item">
                            <img src={item.livro.imagem_url} alt={item.livro.titulo} />
                            <div className="cart-info">
                                <h3>{item.livro.titulo}</h3>
                                <p>R$ {item.livro.preco}</p>
                                <p>Quantidade: {item.quantidade}</p>
                                <button
                                    className="btn-remove"
                                    onClick={() => handleRemover(item.livro.id)}
                                >
                                    Remover
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
                <h3>Total: R$ {total.toFixed(2)}</h3>
                <div className="checkout">
                    <h3>Total: R$ {total.toFixed(2)}</h3>
                    <button className="btn-checkout" onClick={handleCheckout}>
                        Finalizar Pedido
                    </button>
                </div>

            </div>
            <Footer />
        </div>
    );
}

export default Cart;
