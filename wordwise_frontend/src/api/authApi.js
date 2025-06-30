import api from "../services/api";

export async function login(username, password) {
  const response = await api.post("/clientes/login/", {
    username,
    password,
  });
  localStorage.setItem("token", response.data.token);
  localStorage.setItem("username", response.data.username);
  return response.data;
}

export async function logout() {
  const token = localStorage.getItem("token");
  if (!token) return;

  await api.post("/clientes/logout/", {});

  localStorage.removeItem("token");
  localStorage.removeItem("username");
  window.location.href = "/login";
}

export function isAuthenticated() {
  return !!localStorage.getItem("token");
}

export function getUsername() {
  return localStorage.getItem("username");
}
