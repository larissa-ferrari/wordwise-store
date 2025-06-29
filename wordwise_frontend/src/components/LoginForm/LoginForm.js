import React, { useState } from 'react';
import './LoginForm.css';
import mailIcon from '../../assets/icons/icon-mail.svg';
import lockIcon from '../../assets/icons/icon-lock-closed.svg';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Email:', email);
    console.log('Password:', password);
    console.log('Remember Me:', rememberMe);
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
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <label>Email</label>
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
              />
              <label>Senha</label>
            </div>
            <div className="remember-forgot">
              <label>
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />{' '}
                Lembre-se de mim
              </label>
              <a href="#">Esqueceu a senha?</a>
            </div>
            <button type="submit" className="btn">
              Login
            </button>
            <div className="login-register">
              <p>
                Não possui uma conta?{' '}
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
