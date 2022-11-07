var jwt_token = localStorage.getItem('access');
var jwt_token_refresh = localStorage.getItem('refresh');


data = {
    "refresh": jwt_token_refresh
};

if (jwt_token){
    $.ajax({
        type: "POST",
        url: "/api/auth/token/refresh",
        data: data,
        success: function (data) {
            localStorage.setItem('access', data.access);
            const jwt_token = data.access;
            $.ajax({
                type: "POST",
                url: "/api/auth/token/verify",
                data: {"token": jwt_token},
                headers: {
                    "Authorization": "Bearer" + " " + jwt_token
                },
                success: function (data) {
                    var json_string = JSON.stringify(data, null, 2);
                    console.log(data);
                    $('#token').text('Bearer ' + jwt_token);
                    $('#token').css('color', 'green');
                    if(json_string){
                        $('#result').text(" Token verified successfully!");
                    }
                    $('#result').css('color', 'blue').css('white-space', 'pre-line');
                },
                error: function (data) {
                    var result = "please login " + data.responseText;
                    $("#result").text(result).css('color', 'red');
                }
            });
        },
        error: function (data) {
            var result = "please login " + data.responseText;
            $("#result").text(result).css('color', 'red');
        }
    });
} else {
    $('#token').text('Have not login with JWT token!');
}
