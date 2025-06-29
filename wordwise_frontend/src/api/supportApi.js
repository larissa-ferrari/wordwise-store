import api from "../services/api";

export async function listarSuportes() {
  try {
    const response = await api.get("suportes/");
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
}

export async function enviarMensagemSuporte(mensagem) {
  try {
    const response = await api.post("suportes/", { mensagem });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
}
