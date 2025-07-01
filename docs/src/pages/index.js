import React from 'react';
import Layout from '@theme/Layout';
import styles from './index.module.css';

export default function Home() {
  return (
    <Layout
      title="Wordwise - Plataforma de E-commerce de Livros"
      description="Documentação e visão geral do projeto Wordwise"
    >
      <main className={styles.main}>
        <div className={styles.hero}>
          <h1>📚 Wordwise</h1>
          <p>Seu marketplace completo para livros físicos e digitais.</p>
          <div className={styles.buttons}>
            <a
              className={styles.buttonPrimary}
              href="/docs/overview"
            >
              📘 Ver Documentação
            </a>
            <a
              className={styles.buttonSecondary}
              href="http://localhost:3000" // ou o link do seu front
            >
              🛒 Ir para a Loja
            </a>
          </div>
        </div>
      </main>
    </Layout>
  );
}
