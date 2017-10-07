function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    //上传文件
    $.get("/up_information", function(data){
        if ("4101" == data.errcode) {
            location.href = "/login.html";
        }
        else if ("0" == data.errcode) {
            $("#user-name").val(data.data.name);
            if (data.data.avatar) {
                $("#user-avatar").attr("src", data.data.avatar);
            }
        }
    });
    //上传头像
    $("#form-avatar").submit(function (e) {
        // 组织浏览器对于表单的默认行为
        e.preventDefault();
        $('.image_uploading').fadeIn('fast');
        var options = {
            url: "/up_information/avatr",
            method: "post",
            // dataType: "json",
            headers: {
                "X-XSRFTOKEN": getCookie("_xsrf")
            },
            success: function (data) {
                if ("0" == data.errcode) {
                    $('.image_uploading').fadeOut('fast');
                    $("#user-avatar").attr("src", data.data)
                } else if ("4101" == data.errcode) {
                    location.href = "/my";
                }
            }
        };
        $(this).ajaxSubmit(options);
    });
    //上传文件名字
    $("#form-name").submit(function(e){
        e.preventDefault();
        var data = {};
        $(this).serializeArray().map(function(x){data[x.name] = x.value;});
        // var jsonData = JSON.stringify(data);
        $.ajax({
            url:"/up_information/name",
            type:"POST",
            data:data,
            // contentType: "application/json",
            // dataType: "json",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function (data) {
                if ("0" == data.errcode) {
                    $(".error-msg").hide();
                    showSuccessMsg(); // 展示保存成功的页面效果
                } else if ("4001" == data.errcode) {
                    $(".error-msg").show();
                } else if ("4101" == data.errcode) { // 4101代表用户未登录，强制跳转到登录页面
                    location.href = "/my";
                }
            }
        });
    })
})

