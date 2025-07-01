import api from "../services/api";

export async function toggleFavorito(livroId) {
    const response = await api.post(`/favoritos/${livroId}/toggle/`);
    return response.data;
}

export async function listarFavoritos() {
    const response = await api.get("/favoritos/");
    return response.data;
}
