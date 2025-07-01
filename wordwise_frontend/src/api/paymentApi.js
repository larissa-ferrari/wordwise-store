import api from "../services/api";

export async function listarMetodosPagamento() {
    const response = await api.get("pagamentos/");
    return response.data;
}