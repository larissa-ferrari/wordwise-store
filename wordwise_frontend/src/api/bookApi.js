import api from "../services/api";

export async function listarLivros(pagina = 1, limite = 10) {
    try {
        const response = await api.get("livros/", {
            params: {
                page: pagina,
                page_size: limite
            }
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function buscarLivroPorId(id) {
    try {
        const response = await api.get(`livros/${id}/`);
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function buscarLivrosPorTermo(termo) {
    try {
        const response = await api.get("livros/search/", {
            params: {
                titulo: termo
            }
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function listarAvaliacoes(livroId) {
    try {
        const response = await api.get(`livros/${livroId}/avaliacoes/`);
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function adicionarAvaliacao(livroId, nota, comentario) {
    try {
        const response = await api.post("avaliacoes/", {
            livro_id: livroId,
            nota,
            comentario
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function toggleFavorito(livroId) {
    try {
        const response = await api.post(`favoritos/toggle/${livroId}/`);
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function listarFavoritos() {
    try {
        const response = await api.get("favoritos/");
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function listarLivrosDestaque() {
    try {
        const response = await api.get("livros/destaques/");
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}