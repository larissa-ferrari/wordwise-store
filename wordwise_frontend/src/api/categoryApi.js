import api from "../services/api";

export async function obterCategorias() {
    try {
        const response = await api.get("categorias/");
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}