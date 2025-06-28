CREATE DATABASE wordwise;

USE wordwise;

CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    senha VARCHAR(255),
    telefone VARCHAR(20),
    data_nascimento DATE,
    data_cadastro DATETIME,
    tipo_usuario ENUM('cliente', 'administrador') NOT NULL
);

CREATE TABLE cliente (
    id_usuario INT PRIMARY KEY,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE administrador (
    id_usuario INT PRIMARY KEY,
    nivel_acesso VARCHAR(100),
    status BOOLEAN,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE categoria (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255),
    descricao TEXT,
    status BOOLEAN,
    imagem_url VARCHAR(512)
);

CREATE TABLE livro (
    id_livro INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255),
    autor VARCHAR(255),
    editora VARCHAR(255),
    ano_publicacao INT,
    preco DECIMAL(10, 2),
    estoque INT,
    descricao TEXT,
    imagem_url VARCHAR(512),
    isbn VARCHAR(20),
    tipo VARCHAR(100),
    numero_paginas INT,
    idioma VARCHAR(50),
    status BOOLEAN,
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

CREATE TABLE cliente_favoritos (
    id_cliente INT,
    id_livro INT,
    PRIMARY KEY (id_cliente, id_livro),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario),
    FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
);

CREATE TABLE endereco (
    id_endereco INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    rua VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    cep VARCHAR(20),
    pais VARCHAR(50),
    principal BOOLEAN,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario)
);

CREATE TABLE carrinho (
    id_carrinho INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    dt_criacao DATETIME,
    dt_atualizacao DATETIME,
    status VARCHAR(50),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario)
);

CREATE TABLE item_carrinho (
    id_carrinho INT,
    id_livro INT,
    quantidade INT,
    PRIMARY KEY (id_carrinho, id_livro),
    FOREIGN KEY (id_carrinho) REFERENCES carrinho(id_carrinho),
    FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
);

CREATE TABLE pedido (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_endereco INT,
    data_pedido DATETIME,
    status VARCHAR(50),
    valor_total DECIMAL(10, 2),
    forma_pagamento VARCHAR(50),
    cd_rastreamento VARCHAR(100),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario),
    FOREIGN KEY (id_endereco) REFERENCES endereco(id_endereco)
);

CREATE TABLE item_pedido (
    id_pedido INT,
    id_livro INT,
    quantidade INT,
    PRIMARY KEY (id_pedido, id_livro),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
    FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
);

CREATE TABLE avaliacao (
    id_avaliacao INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_livro INT,
    nota INT,
    comentario TEXT,
    data_avaliacao DATETIME,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario),
    FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
);

CREATE TABLE suporte (
    id_suporte INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    mensagem TEXT,
    data_envio DATETIME,
    resposta TEXT,
    data_resposta DATETIME,
    status BOOLEAN,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_usuario)
);

CREATE TABLE banner (
    id_banner INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255),
    imagem_url VARCHAR(512),
    link_destino VARCHAR(512),
    visivel BOOLEAN,
    prioridade INT,
    posicao VARCHAR(100),
    dt_criacao DATETIME
);
