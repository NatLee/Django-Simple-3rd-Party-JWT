$("form").on("submit", function (event) {
    event.preventDefault();

    $.ajax({
        type: "POST",
        url: "/api/auth/token",
        data: $(this).serialize(),
        success: function (data) {
          console.log(data);
          localStorage.setItem('refresh_token', data.refresh);
          localStorage.setItem('access_token', data.access);
          window.location.href = "/api/__hidden_dev_dashboard";
        }
    });
});