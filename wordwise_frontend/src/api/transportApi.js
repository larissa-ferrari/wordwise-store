import api from "../services/api";

export async function listarTransportes() {
    const response = await api.get("transportes/");
    return response.data;
}
