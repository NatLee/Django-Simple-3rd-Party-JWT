$("form").on("submit", function (event) {
  event.preventDefault();

  let action = $(this).find("button[type=submit]:focus").val();

  if (action === 'jwt') {
    // JWT Login logic
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
  } else if (action === 'session') {
    // Session Login logic
    $.ajax({
      type: "POST",
      url: "/api/__hidden_dev_dashboard/login",
      data: $(this).serialize(),
      success: function (data) {
        console.log(data);
        window.location.href = "/api/__hidden_dev_dashboard";
      }
    });
  }
});
