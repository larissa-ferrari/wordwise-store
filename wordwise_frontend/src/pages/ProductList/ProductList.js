import React, { useState, useEffect } from 'react';
import { listarLivros } from '../../api/bookApi';
import Navbar from '../../components/Navbar/Navbar';
import Footer from '../../components/Footer/Footer';
import BookCard from '../../components/BookCard/BookCard';
import './ProductList.css';
import { useLocation } from 'react-router-dom';


function ProductList() {
    const location = useLocation();
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalCount, setTotalCount] = useState(0);
    const productsPerPage = 4;
    const [filtros, setFiltros] = useState({
        autor: "",
        categoria: "",
        tipo: "",
    });

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);

        const newFiltros = {
            autor: queryParams.get("autor") || "",
            categoria: queryParams.get("categoria") || "",
            tipo: queryParams.get("tipo") || "",
        };

        setFiltros(newFiltros);
        setCurrentPage(1);
    }, [location.search]);

    useEffect(() => {
        const fetchProducts = async () => {
            setLoading(true);
            try {
                const data = await listarLivros(currentPage, productsPerPage, filtros);
                setProducts(data.results || []);
                setTotalCount(data.count || 0);
            } catch (error) {
                console.error('Erro ao buscar produtos:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, [currentPage, filtros]);

    const totalPages = Math.ceil(totalCount / productsPerPage);

    return (
        <div>
            <Navbar />
            <div className="product-list-container">
                <h2 className="product-list-title">Todos os Livros</h2>
                <div className="product-grid">
                    {loading ? (
                        <p>Carregando livros...</p>
                    ) : (
                        products.map((book) => (
                            <BookCard
                                key={book.id}
                                id={book.id}
                                title={book.titulo}
                                price={book.preco}
                                image={book.imagem_url}
                            />
                        ))
                    )}
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
