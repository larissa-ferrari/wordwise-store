import api from "../services/api";

export async function criarPedido(dados) {
    const res = await api.post("pedidos/", dados);
    return res.data;
}
