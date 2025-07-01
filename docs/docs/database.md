---
id: database
title: Estrutura do Banco de Dados
---

# 🗄️ Estrutura do Banco de Dados

Principais tabelas:

- **Usuario:** Dados básicos e autenticação.
- **Cliente:** Herança de Usuário.
- **Administrador:** Herança de Usuário.
- **Livro:** Informações detalhadas.
- **Categoria:** Classificação dos livros.
- **Carrinho:** Itens adicionados pelo cliente.
- **Pedido:** Transações e status.
- **ItemPedido:** Detalhes de cada compra.
- **Endereco:** Dados de entrega.
- **Avaliacao:** Feedbacks de usuários.
- **Banner:** Conteúdo promocional.

## Segurança

- Autenticação JWT.
- Validação de entradas.
- Uso de HTTPS.
- Controle de acesso por permissões.
