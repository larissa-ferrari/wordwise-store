import React, { useEffect, useState } from "react";
import { obterCategorias } from "../../api/categoryApi";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "./CategoryCarousel.css";
import { Link } from "react-router-dom";

function CategoryCarousel() {
    const [categorias, setCategorias] = useState([]);

    useEffect(() => {
        async function fetchCategorias() {
            try {
                const data = await obterCategorias();
                setCategorias(data);
            } catch (error) {
                console.error("Erro ao buscar categorias:", error);
            }
        }

        fetchCategorias();
    }, []);

    return (
        <section className="carousel-section">
            <div className="category-carousel">
                <Swiper
                    modules={[Navigation, Pagination]}
                    loop={categorias.length > 6}
                    pagination={{ clickable: true }}
                    navigation
                    breakpoints={{
                        320: { slidesPerView: 2, spaceBetween: 10 },
                        640: { slidesPerView: 3, spaceBetween: 10 },
                        1024: { slidesPerView: 5, spaceBetween: 8 },
                        1280: { slidesPerView: 6, spaceBetween: 8 },
                    }}
                    className="category-swiper"
                >
                    {categorias.map((cat) => (
                        <SwiperSlide key={cat.id}>
                            <Link to={`/livros?categoria=${encodeURIComponent(cat.nome)}`}>
                                <div className="category-item">
                                    <img src={cat.imagem_url} alt={cat.nome} />
                                    <p>{cat.nome.toUpperCase()}</p>
                                </div>
                            </Link>
                        </SwiperSlide>
                    ))}
                </Swiper>
            </div>
        </section>
    );
}

export default CategoryCarousel;
