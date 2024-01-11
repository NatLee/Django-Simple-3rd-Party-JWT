

function logout() {
    window.localStorage.removeItem('access_token');
    window.localStorage.removeItem('refresh_token');
    window.location.href = "/api/__hidden_dev_dashboard";
}

