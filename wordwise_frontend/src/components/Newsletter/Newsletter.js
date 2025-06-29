import React, { useState } from 'react';
import './Newsletter.css';

function Newsletter() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Obrigado, ${nome}! Você se inscreveu com o e-mail: ${email}`);
    setNome('');
    setEmail('');
  };

  return (
    <section className="newsletter-section">
      <h2><strong>Fique</strong> por dentro!</h2>
      <p>Não perca nenhuma novidade, cadastre seu e-mail para receber nossas novidades.</p>
      <form className="newsletter-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Digite seu Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Digite seu e-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit">Inscrever-se</button>
      </form>
    </section>
  );
}

export default Newsletter;
