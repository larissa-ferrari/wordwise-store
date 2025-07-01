import React, { useEffect, useState } from "react";
import { listarAvaliacoes, adicionarAvaliacao } from "../../api/bookApi";
import { isAuthenticated, getUsername } from "../../utils/auth";
import "./Reviews.css";

function Reviews({ livroId }) {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [nota, setNota] = useState(5);
  const [comentario, setComentario] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const [hasReviewed, setHasReviewed] = useState(false);

  useEffect(() => {
    const fetchReviews = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await listarAvaliacoes(livroId);
        setReviews(response);

        if (isAuthenticated()) {
          const user = getUsername();
          const jaAvaliou = response.some(
            (r) => r.cliente?.toLowerCase() === user.toLowerCase()
          );
          setHasReviewed(jaAvaliou);
        }
      } catch (err) {
        setError("Erro ao carregar avaliações.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, [livroId]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isAuthenticated()) {
      setError("Você precisa estar logado para enviar uma avaliação.");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      await adicionarAvaliacao(livroId, nota, comentario);
      setComentario("");
      setNota(5);
      setHasReviewed(true);

      const updated = await listarAvaliacoes(livroId);
      setReviews(updated);
    } catch (err) {
      setError("Erro ao enviar avaliação.");
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="reviews-container">
      <h3>Feedback dos Clientes</h3>
      {loading && <p>Carregando avaliações...</p>}
      {error && <p className="erro-login">{error}</p>}
      {!loading && reviews.length === 0 && <p>Nenhuma avaliação ainda.</p>}

      {reviews.map((review) => (
        <div key={review.id} className="review">
          <div className="review-header">
            <strong>{review.cliente}</strong>
            <span className="rating">
              {"★".repeat(Math.max(0, Math.min(5, Number(review.nota) || 0)))}
              {"☆".repeat(
                5 - Math.max(0, Math.min(5, Number(review.nota) || 0))
              )}
            </span>
          </div>
          <p>{review.comentario}</p>
        </div>
      ))}

      {isAuthenticated() && !hasReviewed && (
        <form onSubmit={handleSubmit} className="review-form">
          <h4>Deixe sua Avaliação</h4>
          <div className="form-group">
            <label>Nota:</label>
            <select
              value={nota}
              onChange={(e) => setNota(Number(e.target.value))}
              required
            >
              <option value={5}>5 - Excelente</option>
              <option value={4}>4 - Muito Bom</option>
              <option value={3}>3 - Bom</option>
              <option value={2}>2 - Regular</option>
              <option value={1}>1 - Ruim</option>
            </select>
          </div>
          <div className="form-group">
            <label>Comentário:</label>
            <textarea
              value={comentario}
              onChange={(e) => setComentario(e.target.value)}
              required
              rows={3}
            />
          </div>
          <button type="submit" disabled={submitting}>
            {submitting ? "Enviando..." : "Enviar Avaliação"}
          </button>
        </form>
      )}

      {!isAuthenticated() && (
        <p className="info-text">Faça login para deixar sua avaliação.</p>
      )}

      {hasReviewed && (
        <p className="info-text">Você já avaliou este produto.</p>
      )}
    </div>
  );
}

export default Reviews;
