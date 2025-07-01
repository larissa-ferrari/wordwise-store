import React, { useState } from "react";
import { criarCliente } from "../../api/customerApi";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import "./Register.css";
import { useNavigate } from "react-router-dom";

function Register() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    email: "",
    cpf: "",
    phone: "",
    birth_date: "",
  });

  const [error, setError] = useState(null);
  const [sucesso, setSucesso] = useState(false);
  const navigate = useNavigate();

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);

    try {
      const payload = {
        user: {
          username: form.username,
          email: form.email,
          phone: form.phone,
          birth_date: form.birth_date,
          is_staff: false,
          is_active: true,
        },
        password: form.password,
        cpf: form.cpf,
      };

      await criarCliente(payload);
      setSucesso(true);

      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      setError(err);
    }
  }

  if (sucesso) {
    return (
      <>
        <main className="cadastro-container">
          <p>Cadastro realizado com sucesso! Faça login para continuar.</p>;
        </main>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="cadastro-container">
        <h1>Cadastro de Cliente</h1>
        {sucesso ? (
          <p className="sucesso-msg">
            Cadastro realizado com sucesso! Faça login para continuar.
          </p>
        ) : (
          <form className="cadastro-form" onSubmit={handleSubmit}>
            <input
              name="username"
              placeholder="Usuário"
              value={form.username}
              onChange={handleChange}
              required
            />
            <input
              name="password"
              type="password"
              placeholder="Senha"
              value={form.password}
              onChange={handleChange}
              required
            />
            <input
              name="email"
              type="email"
              placeholder="E-mail"
              value={form.email}
              onChange={handleChange}
              required
            />
            <input
              name="cpf"
              placeholder="CPF"
              value={form.cpf}
              onChange={handleChange}
              required
            />
            <input
              name="phone"
              placeholder="Telefone"
              value={form.phone}
              onChange={handleChange}
            />
            <input
              name="birth_date"
              type="date"
              placeholder="Data de Nascimento"
              value={form.birth_date}
              onChange={handleChange}
            />
            {error && <p className="error-msg">{JSON.stringify(error)}</p>}
            <button type="submit" className="btn-submit">
              Cadastrar
            </button>
          </form>
        )}
      </main>
      <Footer />
    </>
  );
}

export default Register;
