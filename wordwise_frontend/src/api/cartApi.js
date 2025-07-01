import api from "../services/api";

export async function adicionarAoCarrinho(livroId, quantidade = 1) {
    try {
        const response = await api.post("cart/adicionar/", {
            livro_id: livroId,
            quantidade,
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function removerItemDoCarrinho(livroId) {
    try {
        const response = await api.post(`cart/remover/${livroId}/`);
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function obterCarrinho() {
    try {
        const response = await api.get("cart/recuperar");
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}