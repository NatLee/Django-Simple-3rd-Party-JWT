var jwt_token = localStorage.getItem('access_token');
var jwt_token_refresh = localStorage.getItem('refresh_token');


data = {
    "refresh": jwt_token_refresh
};

if (jwt_token){
    // 這邊刷新是為了測試refresh token的API是否正常
    $.ajax({
        type: "POST",
        url: "/api/auth/token/refresh",
        data: data,
        success: function (data) {
            //console.log(data);
            const new_access_token = data.access; // 預設access token的key為access
            localStorage.setItem('access_token', new_access_token);

            // 這邊是為了測試verify token的API是否正常
            $.ajax({
                type: "POST",
                url: "/api/auth/token/verify",
                data: {"token": new_access_token},
                headers: {
                    "Authorization": "Bearer" + " " + new_access_token
                },
                success: function (data) {
                    var json_string = JSON.stringify(data, null, 2);
                    //console.log(data);
                    $('#token').text('Bearer ' + new_access_token);
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
