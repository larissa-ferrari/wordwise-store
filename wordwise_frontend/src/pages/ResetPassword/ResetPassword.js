import React, { useState } from "react";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { atualizarCliente } from "../../api/customerApi";
import { useNavigate } from "react-router-dom";
import "./ResetPassword.css";

function ResetPassword() {
  const [step, setStep] = useState("email");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const [sucesso, setSucesso] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleEmailSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // MOCK A CHAMADA DE ENVIAR UM EMAIL
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setStep("password");
    } catch (err) {
      setError("Erro ao enviar e-mail. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  async function handlePasswordSubmit(e) {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("As senhas não coincidem.");
      return;
    }

    try {
      // MOCKANDO CLIENTE ID QUE SERIA RETORNADO PELO EMAIL
      const clienteId = 3;

      const payload = {
        user: {
          password,
        },
      };

      await atualizarCliente(clienteId, payload);

      setSucesso(true);

      setTimeout(() => {
        navigate("/login");
      }, 3000);
    } catch (err) {
      setError(err.response?.data || "Erro ao atualizar senha.");
    }
  }

  return (
    <>
      <Navbar />
      <main className="reset-container">
        {step === "email" && !sucesso && (
          <>
            <h1>Redefinir Senha</h1>
            <form className="reset-form" onSubmit={handleEmailSubmit}>
              <input
                name="email"
                type="email"
                placeholder="Digite seu e-mail"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              {error && <p className="error-msg">{error}</p>}
              <button type="submit" className="btn-submit" disabled={loading}>
                {loading ? "Enviando..." : "Enviar"}
              </button>
            </form>
          </>
        )}

        {step === "password" && !sucesso && (
          <>
            <h1>Definir Nova Senha</h1>
            <form className="reset-form" onSubmit={handlePasswordSubmit}>
              <input
                name="password"
                type="password"
                placeholder="Nova Senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <input
                name="confirmPassword"
                type="password"
                placeholder="Confirmar Nova Senha"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
              {error && <p className="error-msg">{error}</p>}
              <button type="submit" className="btn-submit">
                Salvar
              </button>
            </form>
          </>
        )}

        {sucesso && (
          <p className="sucesso-msg">
            Senha atualizada com sucesso! Redirecionando para login...
          </p>
        )}
      </main>
      <Footer />
    </>
  );
}

export default ResetPassword;
