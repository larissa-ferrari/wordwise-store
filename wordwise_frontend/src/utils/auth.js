export function isAuthenticated() {
    return !!localStorage.getItem("token");
}

export function getUsername() {
    return localStorage.getItem("username");
}
