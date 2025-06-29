import React from "react";
import { useParams, Link } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import ShippingCalculator from "../../components/ShippingCalculator/ShippingCalculator";
import Reviews from "../../components/Reviews/Reviews";
import "./ProductDetail.css";
import { FaHeart } from "react-icons/fa";


const products = [
  {
    id: 1,
    title: "Pinoquio",
    price: "54.90",
    author: "Carlo Collodi",
    description: "Uma história clássica sobre um boneco de madeira que ganha vida.",
    image: require("../../assets/books/pinoquio.jpg"),
  },
  {
    id: 2,
    title: "Em Algum Lugar nas Estrelas",
    price: "49.90",
    author: "Clare Vanderpool",
    description: "Uma emocionante aventura repleta de descobertas e amizade.",
    image: require("../../assets/books/estrelas.jpg"),
  },
  {
    id: 3,
    title: "Alice no País das Maravilhas",
    price: "59.90",
    author: "Lewis Carroll",
    description: "Uma viagem mágica e surreal através do País das Maravilhas.",
    image: require("../../assets/books/alice.jpg"),
  },
];

function ProductDetail() {
  const { id } = useParams();
  const product = products.find((p) => p.id === parseInt(id));

  if (!product) {
    return (
      <div>
        <Navbar />
        <div className="product-detail-wrapper">
          <h2>Produto não encontrado.</h2>
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
            <img src={product.image} alt={product.title} />
          </div>
          <div className="product-info">
            <h1 className="product-title">{product.title}</h1>
            <p className="product-author">por {product.author}</p>
            <p className="product-description">{product.description}</p>
            <p className="product-price">R$ {product.price}</p>
            <div className="product-actions">
                <button className="btn-buy">Adicionar ao Carrinho</button>
                <button className="btn-favorite">
                    <FaHeart className="heart-icon" />
                    Favoritar
                </button>
            </div>
            <ShippingCalculator />
            <Link to="/livros" className="back-link">← Voltar para os produtos</Link>
          </div>
        </div>
        <Reviews />
      </div>
      <Footer />
    </div>
  );
}

export default ProductDetail;
