import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import ShippingCalculator from "../../components/ShippingCalculator/ShippingCalculator";
import Reviews from "../../components/Reviews/Reviews";
import { FaHeart } from "react-icons/fa";
import "./ProductDetail.css";
import { buscarLivroPorId } from "../../api/bookApi";
import { adicionarAoCarrinho } from "../../api/cartApi";
import { toast } from "react-toastify"; // se usar notificações

function ProductDetail() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchBook = async () => {
            try {
                const data = await buscarLivroPorId(id);
                setProduct(data);
            } catch (err) {
                console.error("Erro ao buscar livro:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchBook();
    }, [id]);


    const handleAddToCart = async () => {
        try {
            await adicionarAoCarrinho(product.id, 1);
            toast.success("Livro adicionado ao carrinho!");
        } catch (error) {
            console.error("Erro ao adicionar ao carrinho:", error);
            toast.error("Erro ao adicionar ao carrinho.");
        }
    };

    if (loading) {
        return (
            <div>
                <Navbar />
                <div className="product-detail-wrapper">
                    <h2>Carregando...</h2>
                </div>
                <Footer />
            </div>
        );
    }

    if (!product) {
        return (
            <div>
                <Navbar />
                <div className="product-detail-wrapper">
                    <h2>Livro não encontrado.</h2>
                    <Link to="/livros" className="back-link">← Voltar para os produtos</Link>
                </div>
                <Footer />
            </div>
        );
    }

    return (
        <div>
            <Navbar />
            <div className="product-detail-wrapper">
                <div className="product-detail-card">
                    <div className="product-image">
                        <img src={product.imagem_url} alt={product.titulo} />
                    </div>
                    <div className="product-info">
                        <h1 className="product-title">{product.titulo}</h1>
                        <p className="product-author">por {product.autor}</p>
                        <p className="product-description">{product.descricao}</p>
                        <p className="product-price">R$ {product.preco}</p>
                        <div className="product-actions">
                            <button className="btn-buy" onClick={handleAddToCart}>Adicionar ao Carrinho</button>
                            <button className="btn-favorite">
                                <FaHeart className="heart-icon" />
                                Favoritar
                            </button>
                        </div>
                        <ShippingCalculator />
                        <Link to="/livros" className="back-link">← Voltar para os produtos</Link>
                    </div>
                </div>
                <Reviews livroId={product.id} />
            </div>
            <Footer />
        </div>
    );
}

export default ProductDetail;
