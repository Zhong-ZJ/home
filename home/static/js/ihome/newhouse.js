// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return r ? r[1] : undefined;
// }
//
// $(document).ready(function(){
//     $.get("/newhouse", function (data) {
//         if ("0" == data.errcode) {
//             // html = template("area-tmpl", {areas: data.data});
//             // $("#area-id").html(html);
//             // console.log(html);
//             for (var i=0; i<data.data.length; i++) {
//                 $("#area-id").append('<option value="'+data.data[i].area_id+'">'+data.data[i].name+'</option>');
//             }
//         }
//     }, "json")
//
//     $("#form-house-info").submit(function(e){
//         e.preventDefault();
//         $('.popup_con').fadeIn('fast');
//         var formData = $(this).serializeArray();
//         for (var i=0; i<formData.length; i++) {
//             if (!formData[i].value) {
//                 $(".error-msg").show();
//                 return;
//             }
//         }
//         var data = {};
//         $(this).serializeArray().map(function(x){data[x.name] = x.value;});
//         var facility = []; // 用来保存勾选了的设施编号
//         // 通过jquery筛选出勾选了的页面元素
//         // 通过each方法遍历元素
//         $("input:checkbox:checked[name=facility]").each(function(i){facility[i] = this.value;});
//         data.facility = facility;
//         // var jsonData = JSON.stringify(data);
//         $.ajax({
//             url:"/newhouse",
//             type:"POST",
//             data: data,
//             // data: jsonData,
//             // contentType: "application/json",
//             // dataType: "json",
//             headers: {
//                "X-XSRFTOKEN": getCookie("_xsrf"),
//             },
//             success: function (data) {
//                 if ("4101" == data.errcode) {
//                     location.href = "/login.html";
//                 } else if ("0" == data.errcode) {
//                     $(".house-image-cons").append('<img src="'+ data.url+'">');
//                     $('.popup_con').fadeOut('fast');
//                     $("#house-id").val(data.house_id);
//                     $(".error-msg").hide();
//                     $("#form-house-info").hide();
//                     $("#form-house-info").show();
//                 }
//             }
//         });
//
//     });
//     $(this).ajaxSubmit(options);
//     // $("#form-house-info").submit(function(e){
//     //     e.preventDefault();
//     //     $('.popup_con').fadeIn('fast');
//     //     // debugger
//     //     var options = {
//     //         url:"/newhouse",
//     //         type:"POST",
//     //         headers: {
//     //            "X-XSRFTOKEN": getCookie("_xsrf"),
//     //         },
//     //         success: function(data){
//     //             if ("4101" == data.errcode) {
//     //                 location.href = "/login.html";
//     //             } else if ("0" == data.errcode) {
//     //                 $(".house-image-cons").append('<img src="'+ data.url+'">');
//     //                 $('.popup_con').fadeOut('fast');
//     //             }
//     //         }
//     //     };
//     //     $(this).ajaxSubmit(options);
//     // });
// })







function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get("/newhouse", function (data) {
        if ("0" == data.errcode) {
            // html = template("area-tmpl", {areas: data.data});
            // $("#area-id").html(html);
            // console.log(html);
            for (var i=0; i<data.data.length; i++) {
                $("#area-id").append('<option value="'+data.data[i].area_id+'">'+data.data[i].name+'</option>');
            }
        }
    }, "json")

    $("#form-house-info").submit(function(e){
        e.preventDefault();
        // $('.popup_con').fadeIn('fast');
        var formData = $(this).serializeArray();
        for (var i=0; i<formData.length; i++) {
            if (!formData[i].value) {
                $(".error-msg").show();
                return;
            }
        }
        var data = {};
        $(this).serializeArray().map(function(x){data[x.name] = x.value;});
        var facility = []; // 用来保存勾选了的设施编号
        // 通过jquery筛选出勾选了的页面元素
        // 通过each方法遍历元素
        $("input:checkbox:checked[name=facility]").each(function(i){facility[i] = this.value;});
        data.facility = facility;
        // var jsonData = JSON.stringify(data);

        var options={
            url:"/newhouse",
            type:"POST",
            data: data,
            // data: jsonData,
            // contentType: "application/json",
            dataType: "json",
            headers: {
               "X-XSRFTOKEN": getCookie("_xsrf"),
            },
            success: function (data) {
                if ("4101" == data.errcode) {
                    location.href = "/login.html";
                } else if ("0" == data.errcode) {
                    $("#house-id").val(data.house_id);
                    $(".error-msg").hide();
                    $("#form-house-info").hide();
                    $("#form-house-info").show();
                    $(".house-image-cons").append('<img src="'+ data.url+'">');
                    $('.popup_con').fadeOut('fast');
                }else{
                    alert(data.errmsg);
                }
            }
        };
        $(this).ajaxSubmit(options);
    });
})