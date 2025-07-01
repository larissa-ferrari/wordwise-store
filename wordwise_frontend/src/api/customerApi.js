import api from "../services/api";


export async function criarCliente(dadosCliente) {
    try {
        const response = await api.post("clientes/", dadosCliente);
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function buscarCliente(id) {
    try {
        const response = await api.get(`clientes/${id}/`);
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export async function atualizarCliente(id, dadosAtualizados) {
    try {
        const response = await api.patch(`clientes/${id}/`, dadosAtualizados);
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}