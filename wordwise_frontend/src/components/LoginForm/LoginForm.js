import React, { useState } from "react";
import "./LoginForm.css";
import mailIcon from "../../assets/icons/icon-mail.svg";
import lockIcon from "../../assets/icons/icon-lock-closed.svg";
import { login } from "../../api/authApi";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setLoading(true);

    try {
      await login(username, password);
      window.location.href = "/";
    } catch (err) {
      setErro(err.detail || "Falha no login. Verifique seus dados.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-background">
      <div className="wrapper">
        <div className="form-box">
          <h2>Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-box">
              <span className="icon">
                <img src={mailIcon} alt="Email Icon" />
              </span>
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <label>Usuário</label>
            </div>
            <div className="input-box">
              <span className="icon">
                <img src={lockIcon} alt="Lock Icon" />
              </span>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
              <label>Senha</label>
            </div>
            <div className="remember-forgot">
              <a href="/resetar-senha">Esqueceu a senha?</a>
            </div>
            <button type="submit" className="btn">
              {loading ? "Logando..." : "Login"}
            </button>
            {erro && <p className="erro-login">{erro}</p>}
            <div className="login-register">
              <p>
                Não possui uma conta?{" "}
                <a href="/cadastro" className="register-link">
                  Cadastre-se
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
