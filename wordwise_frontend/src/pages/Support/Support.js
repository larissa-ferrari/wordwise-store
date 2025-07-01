import React, { useEffect, useState } from "react";
import { listarSuportes, enviarMensagemSuporte } from "../../api/supportApi";
import { isAuthenticated } from "../../utils/auth";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import "./Support.css";

function Support() {
  const [mensagens, setMensagens] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchMensagens = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await listarSuportes();
        setMensagens(response);
      } catch (err) {
        setError("Erro ao carregar mensagens de suporte.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMensagens();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isAuthenticated()) {
      setError("Você precisa estar logado para enviar uma mensagem.");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      await enviarMensagemSuporte(mensagem);
      setMensagem("");

      const updated = await listarSuportes();
      setMensagens(updated);
    } catch (err) {
      setError("Erro ao enviar mensagem.");
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <Navbar />
      <main className="support-container">
        <h1>Central de Suporte</h1>

        {loading && <p>Carregando mensagens...</p>}
        {error && <p className="error-msg">{error}</p>}

        {!loading && mensagens.length === 0 && (
          <p>Nenhuma mensagem registrada.</p>
        )}

        {!loading &&
          mensagens.map((msg) => (
            <div key={msg.id} className="support-message">
              <div className="support-message-header">
                <div>
                  <strong>Status:</strong>{" "}
                  {msg.status ? (
                    <span className="status-respondido">Respondido</span>
                  ) : (
                    <span className="status-aberto">Aberto</span>
                  )}
                </div>
                <div>
                  <span className="data-envio">
                    Enviada em: {new Date(msg.data_envio).toLocaleDateString()}
                  </span>
                  {msg.data_resposta && (
                    <span className="data-resposta">
                      {" "}
                      | Respondida em:{" "}
                      {new Date(msg.data_resposta).toLocaleDateString()}
                    </span>
                  )}
                </div>
              </div>
              <div className="mensagem-bloco">
                <p>
                  <strong>Mensagem:</strong>
                </p>
                <p>{msg.mensagem}</p>
              </div>
              {msg.resposta && (
                <div className="resposta-bloco">
                  <p>
                    <strong>Resposta:</strong>
                  </p>
                  <p>{msg.resposta}</p>
                </div>
              )}
            </div>
          ))}

        {isAuthenticated() ? (
          <form className="support-form" onSubmit={handleSubmit}>
            <textarea
              placeholder="Digite sua mensagem de suporte..."
              value={mensagem}
              onChange={(e) => setMensagem(e.target.value)}
              required
              rows={4}
            />
            <button type="submit" disabled={submitting}>
              {submitting ? "Enviando..." : "Enviar Mensagem"}
            </button>
          </form>
        ) : (
          <p className="info-text">Faça login para enviar uma mensagem.</p>
        )}
      </main>
      <Footer />
    </>
  );
}

export default Support;
